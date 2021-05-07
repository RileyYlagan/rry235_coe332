# worker.py
from jobs import q, update_job_status, rd_data, rd_jobs, rd_imgs
import time
from hotqueue import HotQueue
import json
import os
import redis
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np

redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
    raise Exception()


#rd_data = redis.StrictRedis(host=redis_ip, port=6379, db=0) # data db
#rd_jobs = redis.StrictRedis(host=redis_ip, port=6379, db=1,decode_responses=True) # jobs db
#q = HotQueue('queue', host=redis_ip, port=6379, db=2)


@q.worker
def execute_job(jid):

    update_job_status(jid, 'in progress')
    
    # Get player info from redis db/ Get job data from redis db
    player_info = json.loads(rd_data.get('Player_Info'))

    #job = {key.decode('utf-8') : value.decode('utf-8') for key, value in rd.hgetall(jid).items()}
    #min_points = job['min_points']
    #max_points = job['max_points']
    job_id = 'job.{}'.format(jid)
    ## THESE LINES DONT WORK ????
    min_points = float(rd_jobs.hget(job_id,'min_points').decode('utf-8'))
    max_points = float(rd_jobs.hget(job_id,'max_points').decode('utf-8'))

    # Total points scored by players born in each U.S State
    # Stats collected up until 2017
    # Gather the total points for each state:
    player_info_list = player_info["Players"]
    state_names = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
    "Connecticut","DC","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
    "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
    "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
    "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
    "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
    "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
    "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]  # 50 States + DC
    points_by_state = []

    for state in state_names:
        index = [index for (index,d) in enumerate(player_info_list) if d['State'] == state]
        points = 0.0
        for i in index:
            points = points + player_info_list[i]["Pts"]
        points_by_state.append(points)
    states_points_dict = []
    for i in range(len(state_names)):
        states_points_dict.append({"state":state_names[i],"points":points_by_state[i]})

    # Sort states by point in descending order
    sorted_states_dict = sorted(states_points_dict, key = lambda i: i['points'], reverse=True)
    sorted_states_list = []
    sorted_points_list = []
    for i in range(len(sorted_states_dict)):
        if(sorted_states_dict[i]["points"] > min_points and sorted_states_dict[i]["points"] < max_points):
            sorted_states_list.append(sorted_states_dict[i]["state"])
            sorted_points_list.append(sorted_states_dict[i]["points"])


    # Plot Graph
    colors = ['b','g','r','c','m','y',
            'b','g','r','c','m','y',
            'b','g','r','c','m','y',
            'b','g','r','c','m','y',
            'b','g','r','c','m','y',
            'b','g','r','c','m','y',
            'b','g','r','c','m','y',
            'b','g','r','c','m','y',
            'b','g','r']
    fig, ax = plt.subplots(figsize=(15,15))
    y_pos = np.arange(len(sorted_states_list))

    ax.barh(2*y_pos,sorted_points_list,height=2,align='center',color = colors[:len(sorted_points_list)])
    ax.set_yticks(2*y_pos)
    ax.set_yticklabels(sorted_states_list)
    ax.invert_yaxis()
    ax.set_xlabel('Points Scored',fontsize='xx-large')
    ax.set_title('Total points scored by NBA/ABA players born in each U.S State',fontsize='xx-large')
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.xlim([0,max(sorted_points_list)*1.25])

    # Add x, y gridlines
    ax.grid(b=True, color='grey',
            linestyle='-.', linewidth=0.5,
            alpha=0.2)
    # Add annotation to bars
    for i in ax.patches:
        plt.text(i.get_width()*1.025, i.get_y()+i.get_height()/1.75,
                str(round((i.get_width()), 2)),
                color='grey')

    ax.figure.savefig('/plot.png')

    with open('/plot.png','rb') as f:
        img = f.read()



    rd_imgs.hset(jid,'image',img)
    update_job_status(jid, 'complete')
    
    
execute_job()