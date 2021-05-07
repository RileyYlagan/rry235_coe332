# jobs.py
from hotqueue import HotQueue
import datetime
import redis 
import uuid
import os # allows us to change ip without rebuilding

redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
    raise Exception()
    
rd_data = redis.StrictRedis(host=redis_ip, port=6379, db=0) # data db
rd_jobs = redis.StrictRedis(host=redis_ip, port=6379, db=1)
rd_imgs = redis.StrictRedis(host=redis_ip, port=6379, db=3)  # jobs db
q = HotQueue('queue', host=redis_ip, port=6379, db=2)


def _generate_jid():
    return str(uuid.uuid4())

def _generate_job_key(jid):
    return 'job.{}'.format(jid)

def _instantiate_job(jid, status, datetime, min_points, max_points):
    if type(jid) == str:
        return {'id': jid,
                'status': status,
                'datetime': datetime,
                'min_points': min_points,
                'max_points': max_points
        }
    return {'id': jid.decode('utf-8'),
            'status': status.decode('utf-8'),
            'datetime' : datetime.decode('utf-8'),
            'min_points': min_points.decode('utf-8'),
            'max_points': max_points.decode('utf-8')
    }

def _save_job(job_key, job_dict):
    """Save a job object in the Redis database."""
    rd_jobs.hmset(job_key, job_dict)

def _queue_job(jid):
    """Add a job to the redis queue."""
    q.put(jid)

def add_job(datetime, min_points, max_points, status="submitted"):
    """Add a job to the redis queue."""
    jid = _generate_jid()
    job_dict = _instantiate_job(jid, status, datetime, min_points, max_points)
    # update call to save_job:
    _save_job(_generate_job_key(jid),job_dict)
    # update call to queue_job:
    _queue_job(jid)
    return job_dict

def update_job_status(jid, status_new):
    """Update the status of job with job id `jid` to status `status`."""
    jid, status, datetime, min_points, max_points = rd_jobs.hmget(_generate_job_key(jid), 'id', 'status', 'datetime', 'min_points', 'max_points')
    job = _instantiate_job(jid, status, datetime, min_points, max_points)
    if job:
        job['status'] = status_new
        _save_job(_generate_job_key(job['id']), job)
    else:
        raise Exception()