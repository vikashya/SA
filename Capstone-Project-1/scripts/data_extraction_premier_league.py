import requests
from bs4 import BeautifulSoup
import json
import urllib.request
import os

l_position = {'D':'Defenders','M':'Midfielders','F':'Forwards','G':'Goalkeeper'}
seasonname='2018-19'
json_files_path='data/'+seasonname
data=json_files_path+'/premier_league_data.json'
json_files = [pos_json for pos_json in os.listdir(json_files_path) if pos_json.endswith('.json')]
#json_files = ['0-page.json']
#jresponse = json.load(response)
new_json={}
json_element={}
i=0

def get_lineup (str1):
    page = requests.get(str1)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='mainContent')
    section_elems = results.find_all('section', class_='mcContent')
    for elem in section_elems:
        matchlineup = elem.find('div', class_='mcTabsContainer')
        matchlineupd = matchlineup["data-fixture"]
        jresponselineup = json.loads(matchlineupd) 
        return jresponselineup

def get_dtls (data1 , teamid):
    for d in data1:
        if (str(d['teamId']) == teamid):
            return d
            
def get_stats (data1 , statname):
    for d in data1:
        if (d['name'] == statname):
            return int(d['value'])

def get_gs_count (data1 , pid):
    i=0
    if (pid !=-1):
        for d in data1[1:]:
            try:
                if ( int(d['personId'])==int(pid) and d['type']=='G'):
                    i=i+1
            except KeyError:
                continue
    elif (pid==-1):
        for d in data1[1:]:
            try:
                if ( d['type']=='O'):
                    i=i+1
            except KeyError:
                continue        
    return i

def get_yc_count (data1 , pid):
    yc_count=0
    for d in data1[1:]:
        try:
            if ( int(d['personId'])==int(pid) and d['type']=='B' and d['description']=='Y'):
                yc_count=yc_count+1
        except KeyError:
            continue
    return yc_count

def get_match_stat (mid):
    with open(json_files_path+'/jsons/'+mid+'.json') as stat_file:
        data = json.load(stat_file)
        return data
        
for file in json_files:
    with open(json_files_path+'/'+file) as jdata:
        print ('Reading file:'+ file)
        jresponse = json.load(jdata)
        for entry in jresponse['content']:
            json_element={}
            new_json[i]=[]
            #statresponse = urllib.request.urlopen('https://footballapi.pulselive.com/football/stats/match/'+str(int(entry['id'])))
            #jstatresponse = json.load(statresponse) 
            jstatresponse = get_match_stat(str(int(entry['id'])))
            t_h_id = str(int(entry['teams'][0]['team']['id']))
            t_a_id = str(int(entry['teams'][1]['team']['id']))
            json_element['gameid'] =entry['id'] 
            print ('Processing match id:'+ str(entry['id']))
            json_element['seasonlabel'] =entry['gameweek']['compSeason']['label']
            json_element['gameweekid'] =entry['gameweek']['id']
            json_element['gameweeknum'] =entry['gameweek']['gameweek']
            json_element['gamedate'] =entry['kickoff']['label']
            json_element['team_h_id'] =entry['teams'][0]['team']['id']
            json_element['team_h'] =entry['teams'][0]['team']['name']
            json_element['team_a_id'] =entry['teams'][1]['team']['id']
            json_element['team_a'] =entry['teams'][1]['team']['name']    
            json_element['score_h'] =entry['teams'][0]['score'] 
            json_element['score_a'] =entry['teams'][1]['score'] 
            json_element['groundid'] =entry['ground']['id']      
            json_element['groundname'] =entry['ground']['name']  
            json_element['groundcity'] =entry['ground']['city']  
            json_element['matchstatus'] =entry['status']
            json_element['matchoutcome'] =entry['outcome']     
            json_element['matchphase'] =entry['phase'] 
            json_element['attendance'] =entry['attendance'] 
            json_element['extraTime'] =entry['extraTime']      
            json_element['shootout'] =entry['shootout'] 
            json_element['matchtime'] =entry['clock'] ['secs'] 
            #print (t_h_id + '-' + str(entry['id']))
            #print (jstatresponse['data'][t_h_id]['M'])
            json_element['formation_h'] = get_stats(jstatresponse['data'][t_h_id]['M'], 'formation_used')
            json_element['formation_a'] = get_stats(jstatresponse['data'][t_a_id]['M'], 'formation_used')
            json_element['tot_dist_m_h'] = get_stats(jstatresponse['data'][t_h_id]['M'], 'total_distance_in_m')
            json_element['tot_dist_m_a'] = get_stats(jstatresponse['data'][t_a_id]['M'], 'total_distance_in_m') 
            json_element['clearance_h'] = get_stats(jstatresponse['data'][t_h_id]['M'], 'total_clearance')            
            json_element['clearance_a'] = get_stats(jstatresponse['data'][t_a_id]['M'], 'total_clearance')            
            json_element['pass_h'] = get_stats(jstatresponse['data'][t_h_id]['M'], 'total_pass')                
            json_element['pass_a'] = get_stats(jstatresponse['data'][t_a_id]['M'], 'total_pass')  
            json_element['touches_h'] = get_stats(jstatresponse['data'][t_h_id]['M'], 'touches')                
            json_element['touches_a'] = get_stats(jstatresponse['data'][t_a_id]['M'], 'touches')
            json_element['touches_opp_box_h'] = get_stats(jstatresponse['data'][t_h_id]['M'], 'touches_in_opp_box')                
            json_element['touches_opp_box_a'] = get_stats(jstatresponse['data'][t_a_id]['M'], 'touches_in_opp_box')                
            json_element['possession_pct_h'] = get_stats(jstatresponse['data'][t_h_id]['M'], 'possession_percentage')                
            json_element['possession_pct_a'] = get_stats(jstatresponse['data'][t_a_id]['M'], 'possession_percentage')     
            json_element['poss_lost_ctrl_h'] = get_stats(jstatresponse['data'][t_h_id]['M'], 'poss_lost_ctrl')            
            json_element['poss_lost_ctrl_a'] = get_stats(jstatresponse['data'][t_a_id]['M'], 'poss_lost_ctrl')                
            json_element['total_tackle_h'] = get_stats(jstatresponse['data'][t_h_id]['M'], 'total_tackle')                
            json_element['total_tackle_a'] = get_stats(jstatresponse['data'][t_a_id]['M'], 'total_tackle')                
            json_element['won_tackle_h'] = get_stats(jstatresponse['data'][t_h_id]['M'], 'won_tackle')                
            json_element['won_tackle_a'] = get_stats(jstatresponse['data'][t_a_id]['M'], 'won_tackle')                
            json_element['tot_long_balls_h'] = get_stats(jstatresponse['data'][t_h_id]['M'], 'total_long_balls')                
            json_element['tot_long_balls_a'] = get_stats(jstatresponse['data'][t_a_id]['M'], 'total_long_balls')                
            json_element['tot_offside_h'] = get_stats(jstatresponse['data'][t_h_id]['M'], 'total_offside')                
            json_element['tot_offside_a'] = get_stats(jstatresponse['data'][t_a_id]['M'], 'total_offside')                
            json_element['shot_off_target_h'] = get_stats(jstatresponse['data'][t_h_id]['M'], 'shot_off_target')                
            json_element['shot_off_target_a'] = get_stats(jstatresponse['data'][t_a_id]['M'], 'shot_off_target')                
            json_element['corner_taken_h'] = get_stats(jstatresponse['data'][t_h_id]['M'], 'corner_taken')                
            json_element['corner_taken_a'] = get_stats(jstatresponse['data'][t_a_id]['M'], 'corner_taken')                
            json_element['interception_h'] = get_stats(jstatresponse['data'][t_h_id]['M'], 'interception')                
            json_element['interception_a'] = get_stats(jstatresponse['data'][t_a_id]['M'], 'interception')                
            json_element['first_half_goals_h'] = get_stats(jstatresponse['data'][t_h_id]['M'], 'first_half_goals')                
            json_element['first_half_goals_a'] = get_stats(jstatresponse['data'][t_a_id]['M'], 'first_half_goals')                
            json_element['goals_openplay_h'] = get_stats(jstatresponse['data'][t_h_id]['M'], 'goals_openplay')                
            json_element['goals_openplay_a'] = get_stats(jstatresponse['data'][t_a_id]['M'], 'goals_openplay')                
            json_element['big_chance_created_h'] = get_stats(jstatresponse['data'][t_h_id]['M'], 'big_chance_created')                
            json_element['big_chance_created_a'] = get_stats(jstatresponse['data'][t_a_id]['M'], 'big_chance_created')                
            json_element['big_chance_scored_h'] = get_stats(jstatresponse['data'][t_h_id]['M'], 'big_chance_scored')                
            json_element['big_chance_scored_a'] = get_stats(jstatresponse['data'][t_a_id]['M'], 'big_chance_scored')                
            json_element['big_chance_missed_h'] = get_stats(jstatresponse['data'][t_h_id]['M'], 'big_chance_missed')                
            json_element['big_chance_missed_a'] = get_stats(jstatresponse['data'][t_a_id]['M'], 'big_chance_missed')                
            json_element['own_goal_accrued_h'] = get_stats(jstatresponse['data'][t_h_id]['M'], 'own_goal_accrued')                
            json_element['own_goal_accrued_a'] = get_stats(jstatresponse['data'][t_a_id]['M'], 'own_goal_accrued')                
            json_element['saves_h'] = get_stats(jstatresponse['data'][t_h_id]['M'], 'saves')                
            json_element['saves_a'] = get_stats(jstatresponse['data'][t_a_id]['M'], 'saves')                
            json_element['tot_yel_card_h'] = get_stats(jstatresponse['data'][t_h_id]['M'], 'total_yel_card')                
            json_element['tot_yel_card_a'] = get_stats(jstatresponse['data'][t_a_id]['M'], 'total_yel_card')                
            json_element['forward_goals_h'] = get_stats(jstatresponse['data'][t_h_id]['M'], 'forward_goals')                
            json_element['forward_goals_a'] = get_stats(jstatresponse['data'][t_a_id]['M'], 'forward_goals')                
            json_element['defender_goals_h'] = get_stats(jstatresponse['data'][t_h_id]['M'], 'defender_goals')                
            json_element['defender_goals_a'] = get_stats(jstatresponse['data'][t_a_id]['M'], 'defender_goals')                
            json_element['midfielder_goals_h'] = get_stats(jstatresponse['data'][t_h_id]['M'], 'midfielder_goals')                
            json_element['midfielder_goals_a'] = get_stats(jstatresponse['data'][t_a_id]['M'], 'midfielder_goals')                
            json_element['subs_made_h'] = get_stats(jstatresponse['data'][t_h_id]['M'], 'subs_made')                
            json_element['subs_made_a'] = get_stats(jstatresponse['data'][t_a_id]['M'], 'subs_made')
            lineup1 = get_lineup ('https://www.premierleague.com/match/'+str(int(entry['id'])))
            json_element['player1_name_h'] = get_dtls(lineup1['teamLists'],t_h_id)['lineup'][0]['name']['display']
            json_element['player2_name_h'] = get_dtls(lineup1['teamLists'],t_h_id)['lineup'][1]['name']['display']
            json_element['player3_name_h'] = get_dtls(lineup1['teamLists'],t_h_id)['lineup'][2]['name']['display']
            json_element['player4_name_h'] = get_dtls(lineup1['teamLists'],t_h_id)['lineup'][3]['name']['display']
            json_element['player5_name_h'] = get_dtls(lineup1['teamLists'],t_h_id)['lineup'][4]['name']['display']
            json_element['player6_name_h'] = get_dtls(lineup1['teamLists'],t_h_id)['lineup'][5]['name']['display']
            json_element['player7_name_h'] = get_dtls(lineup1['teamLists'],t_h_id)['lineup'][6]['name']['display']
            json_element['player8_name_h'] = get_dtls(lineup1['teamLists'],t_h_id)['lineup'][7]['name']['display']
            json_element['player9_name_h'] = get_dtls(lineup1['teamLists'],t_h_id)['lineup'][8]['name']['display']
            json_element['player10_name_h'] = get_dtls(lineup1['teamLists'],t_h_id)['lineup'][9]['name']['display']
            json_element['player11_name_h'] = get_dtls(lineup1['teamLists'],t_h_id)['lineup'][10]['name']['display'] if (len(get_dtls(lineup1['teamLists'],t_h_id)['lineup'])>10 ) else 'Not Available'   
            json_element['player12_name_h'] = get_dtls(lineup1['teamLists'],t_h_id)['substitutes'][0]['name']['display']    
            json_element['player13_name_h'] = get_dtls(lineup1['teamLists'],t_h_id)['substitutes'][1]['name']['display']    
            json_element['player14_name_h'] = get_dtls(lineup1['teamLists'],t_h_id)['substitutes'][2]['name']['display']    
            json_element['player15_name_h'] = get_dtls(lineup1['teamLists'],t_h_id)['substitutes'][3]['name']['display']    
            json_element['player16_name_h'] = get_dtls(lineup1['teamLists'],t_h_id)['substitutes'][4]['name']['display']    
            json_element['player17_name_h'] = get_dtls(lineup1['teamLists'],t_h_id)['substitutes'][5]['name']['display'] if (len(get_dtls(lineup1['teamLists'],t_h_id)['substitutes'])>5 ) else 'Not Available'   
            json_element['player18_name_h'] = get_dtls(lineup1['teamLists'],t_h_id)['substitutes'][6]['name']['display'] if (len(get_dtls(lineup1['teamLists'],t_h_id)['substitutes'])>6 ) else 'Not Available'
            json_element['player1_name_a'] = get_dtls(lineup1['teamLists'],t_a_id)['lineup'][0]['name']['display']
            json_element['player2_name_a'] = get_dtls(lineup1['teamLists'],t_a_id)['lineup'][1]['name']['display']
            json_element['player3_name_a'] = get_dtls(lineup1['teamLists'],t_a_id)['lineup'][2]['name']['display']
            json_element['player4_name_a'] = get_dtls(lineup1['teamLists'],t_a_id)['lineup'][3]['name']['display']
            json_element['player5_name_a'] = get_dtls(lineup1['teamLists'],t_a_id)['lineup'][4]['name']['display']
            json_element['player6_name_a'] = get_dtls(lineup1['teamLists'],t_a_id)['lineup'][5]['name']['display']
            json_element['player7_name_a'] = get_dtls(lineup1['teamLists'],t_a_id)['lineup'][6]['name']['display']
            json_element['player8_name_a'] = get_dtls(lineup1['teamLists'],t_a_id)['lineup'][7]['name']['display']
            json_element['player9_name_a'] = get_dtls(lineup1['teamLists'],t_a_id)['lineup'][8]['name']['display']
            json_element['player10_name_a'] = get_dtls(lineup1['teamLists'],t_a_id)['lineup'][9]['name']['display']
            json_element['player11_name_a'] = get_dtls(lineup1['teamLists'],t_a_id)['lineup'][10]['name']['display'] if (len(get_dtls(lineup1['teamLists'],t_a_id)['lineup'])>10 ) else 'Not Available'   
            json_element['player12_name_a'] = get_dtls(lineup1['teamLists'],t_a_id)['substitutes'][0]['name']['display']    
            json_element['player13_name_a'] = get_dtls(lineup1['teamLists'],t_a_id)['substitutes'][1]['name']['display']    
            json_element['player14_name_a'] = get_dtls(lineup1['teamLists'],t_a_id)['substitutes'][2]['name']['display']    
            json_element['player15_name_a'] = get_dtls(lineup1['teamLists'],t_a_id)['substitutes'][3]['name']['display']    
            json_element['player16_name_a'] = get_dtls(lineup1['teamLists'],t_a_id)['substitutes'][4]['name']['display']    
            json_element['player17_name_a'] = get_dtls(lineup1['teamLists'],t_a_id)['substitutes'][5]['name']['display'] if (len(get_dtls(lineup1['teamLists'],t_a_id)['substitutes'])>5 ) else 'Not Available'   
            json_element['player18_name_a'] = get_dtls(lineup1['teamLists'],t_a_id)['substitutes'][6]['name']['display'] if (len(get_dtls(lineup1['teamLists'],t_a_id)['substitutes'])>6 ) else 'Not Available'
            json_element['player1_role_h'] = l_position[get_dtls(lineup1['teamLists'],t_h_id)['lineup'][0]['matchPosition']]
            json_element['player2_role_h'] = l_position[get_dtls(lineup1['teamLists'],t_h_id)['lineup'][1]['matchPosition']]
            json_element['player3_role_h'] = l_position[get_dtls(lineup1['teamLists'],t_h_id)['lineup'][2]['matchPosition']]
            json_element['player4_role_h'] = l_position[get_dtls(lineup1['teamLists'],t_h_id)['lineup'][3]['matchPosition']]
            json_element['player5_role_h'] = l_position[get_dtls(lineup1['teamLists'],t_h_id)['lineup'][4]['matchPosition']]
            json_element['player6_role_h'] = l_position[get_dtls(lineup1['teamLists'],t_h_id)['lineup'][5]['matchPosition']]
            json_element['player7_role_h'] = l_position[get_dtls(lineup1['teamLists'],t_h_id)['lineup'][6]['matchPosition']]
            json_element['player8_role_h'] = l_position[get_dtls(lineup1['teamLists'],t_h_id)['lineup'][7]['matchPosition']]
            json_element['player9_role_h'] = l_position[get_dtls(lineup1['teamLists'],t_h_id)['lineup'][8]['matchPosition']]
            json_element['player10_role_h'] = l_position[get_dtls(lineup1['teamLists'],t_h_id)['lineup'][9]['matchPosition']]
            json_element['player11_role_h'] = l_position[get_dtls(lineup1['teamLists'],t_h_id)['lineup'][10]['matchPosition']] if (len(get_dtls(lineup1['teamLists'],t_h_id)['lineup'])>10 ) else 'Not Available'   
            json_element['player12_role_h'] = l_position[get_dtls(lineup1['teamLists'],t_h_id)['substitutes'][0]['matchPosition']]    
            json_element['player13_role_h'] = l_position[get_dtls(lineup1['teamLists'],t_h_id)['substitutes'][1]['matchPosition']]    
            json_element['player14_role_h'] = l_position[get_dtls(lineup1['teamLists'],t_h_id)['substitutes'][2]['matchPosition']]    
            json_element['player15_role_h'] = l_position[get_dtls(lineup1['teamLists'],t_h_id)['substitutes'][3]['matchPosition']]    
            json_element['player16_role_h'] = l_position[get_dtls(lineup1['teamLists'],t_h_id)['substitutes'][4]['matchPosition']]    
            json_element['player17_role_h'] = l_position[get_dtls(lineup1['teamLists'],t_h_id)['substitutes'][5]['matchPosition']]  if (len(get_dtls(lineup1['teamLists'],t_h_id)['substitutes'])>5 ) else 'Not Available'     
            json_element['player18_role_h'] =  l_position[get_dtls(lineup1['teamLists'],t_h_id)['substitutes'][6]['matchPosition']] if (len(get_dtls(lineup1['teamLists'],t_h_id)['substitutes'])>6 ) else 'Not Available'   
            json_element['player1_role_a'] = l_position[get_dtls(lineup1['teamLists'],t_a_id)['lineup'][0]['matchPosition']]
            json_element['player2_role_a'] = l_position[get_dtls(lineup1['teamLists'],t_a_id)['lineup'][1]['matchPosition']]
            json_element['player3_role_a'] = l_position[get_dtls(lineup1['teamLists'],t_a_id)['lineup'][2]['matchPosition']]
            json_element['player4_role_a'] = l_position[get_dtls(lineup1['teamLists'],t_a_id)['lineup'][3]['matchPosition']]
            json_element['player5_role_a'] = l_position[get_dtls(lineup1['teamLists'],t_a_id)['lineup'][4]['matchPosition']]
            json_element['player6_role_a'] = l_position[get_dtls(lineup1['teamLists'],t_a_id)['lineup'][5]['matchPosition']]
            json_element['player7_role_a'] = l_position[get_dtls(lineup1['teamLists'],t_a_id)['lineup'][6]['matchPosition']]
            json_element['player8_role_a'] = l_position[get_dtls(lineup1['teamLists'],t_a_id)['lineup'][7]['matchPosition']]
            json_element['player9_role_a'] = l_position[get_dtls(lineup1['teamLists'],t_a_id)['lineup'][8]['matchPosition']]
            json_element['player10_role_a'] = l_position[get_dtls(lineup1['teamLists'],t_a_id)['lineup'][9]['matchPosition']]
            json_element['player11_role_a'] = l_position[get_dtls(lineup1['teamLists'],t_a_id)['lineup'][10]['matchPosition']] if (len(get_dtls(lineup1['teamLists'],t_a_id)['lineup'])>10 ) else 'Not Available'   
            json_element['player12_role_a'] = l_position[get_dtls(lineup1['teamLists'],t_a_id)['substitutes'][0]['matchPosition']]    
            json_element['player13_role_a'] = l_position[get_dtls(lineup1['teamLists'],t_a_id)['substitutes'][1]['matchPosition']]    
            json_element['player14_role_a'] = l_position[get_dtls(lineup1['teamLists'],t_a_id)['substitutes'][2]['matchPosition']]    
            json_element['player15_role_a'] = l_position[get_dtls(lineup1['teamLists'],t_a_id)['substitutes'][3]['matchPosition']]    
            json_element['player16_role_a'] = l_position[get_dtls(lineup1['teamLists'],t_a_id)['substitutes'][4]['matchPosition']]    
            json_element['player17_role_a'] = l_position[get_dtls(lineup1['teamLists'],t_a_id)['substitutes'][5]['matchPosition']]  if (len(get_dtls(lineup1['teamLists'],t_a_id)['substitutes'])>5) else 'Not Available'  
            json_element['player18_role_a'] =  l_position[get_dtls(lineup1['teamLists'],t_a_id)['substitutes'][6]['matchPosition']] if (len(get_dtls(lineup1['teamLists'],t_a_id)['substitutes'])>6) else 'Not Available'
            json_element['player1_GS_h'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['lineup'][0]['id'])        
            json_element['player2_GS_h'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['lineup'][1]['id'])        
            json_element['player3_GS_h'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['lineup'][2]['id'])            
            json_element['player4_GS_h'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['lineup'][3]['id'])                
            json_element['player5_GS_h'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['lineup'][4]['id'])                
            json_element['player6_GS_h'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['lineup'][5]['id'])                
            json_element['player7_GS_h'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['lineup'][6]['id'])    
            json_element['player8_GS_h'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['lineup'][7]['id'])        
            json_element['player9_GS_h'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['lineup'][8]['id'])        
            json_element['player10_GS_h'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['lineup'][9]['id'])        
            json_element['player11_GS_h'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['lineup'][10]['id'])   if (len(get_dtls(lineup1['teamLists'],t_h_id)['lineup'])>10 ) else 0   
            json_element['player12_GS_h'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['substitutes'][0]['id'])        
            json_element['player13_GS_h'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['substitutes'][1]['id'])            
            json_element['player14_GS_h'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['substitutes'][2]['id'])            
            json_element['player15_GS_h'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['substitutes'][3]['id'])            
            json_element['player16_GS_h'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['substitutes'][4]['id'])            
            json_element['player17_GS_h'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['substitutes'][5]['id']) if (len(get_dtls(lineup1['teamLists'],t_h_id)['substitutes'])>5 ) else 0
            json_element['player18_GS_h'] =  get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['substitutes'][6]['id']) if (len(get_dtls(lineup1['teamLists'],t_h_id)['substitutes'])>6 ) else 0
            json_element['player1_GS_a'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['lineup'][0]['id'])        
            json_element['player2_GS_a'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['lineup'][1]['id'])        
            json_element['player3_GS_a'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['lineup'][2]['id'])            
            json_element['player4_GS_a'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['lineup'][3]['id'])                
            json_element['player5_GS_a'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['lineup'][4]['id'])                
            json_element['player6_GS_a'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['lineup'][5]['id'])                
            json_element['player7_GS_a'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['lineup'][6]['id'])    
            json_element['player8_GS_a'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['lineup'][7]['id'])        
            json_element['player9_GS_a'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['lineup'][8]['id'])        
            json_element['player10_GS_a'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['lineup'][9]['id'])        
            json_element['player11_GS_a'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['lineup'][10]['id'])  if (len(get_dtls(lineup1['teamLists'],t_a_id)['lineup'])>10 ) else 0  
            json_element['player12_GS_a'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['substitutes'][0]['id'])        
            json_element['player13_GS_a'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['substitutes'][1]['id'])            
            json_element['player14_GS_a'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['substitutes'][2]['id'])            
            json_element['player15_GS_a'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['substitutes'][3]['id'])            
            json_element['player16_GS_a'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['substitutes'][4]['id'])            
            json_element['player17_GS_a'] = get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['substitutes'][5]['id']) if (len(get_dtls(lineup1['teamLists'],t_a_id)['substitutes'])>5 ) else 0
            json_element['player18_GS_a'] =  get_gs_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['substitutes'][6]['id']) if (len(get_dtls(lineup1['teamLists'],t_a_id)['substitutes'])>6 ) else 0
            json_element['player1_YC_h'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['lineup'][0]['id'])            
            json_element['player2_YC_h'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['lineup'][1]['id'])            
            json_element['player3_YC_h'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['lineup'][2]['id'])            
            json_element['player4_YC_h'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['lineup'][3]['id'])            
            json_element['player5_YC_h'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['lineup'][4]['id'])            
            json_element['player6_YC_h'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['lineup'][5]['id'])                
            json_element['player7_YC_h'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['lineup'][6]['id'])            
            json_element['player8_YC_h'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['lineup'][7]['id'])            
            json_element['player9_YC_h'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['lineup'][8]['id'])            
            json_element['player10_YC_h'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['lineup'][9]['id'])            
            json_element['player11_YC_h'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['lineup'][10]['id'])  if (len(get_dtls(lineup1['teamLists'],t_h_id)['lineup'])>10 ) else 0             
            json_element['player12_YC_h'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['substitutes'][0]['id'])            
            json_element['player13_YC_h'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['substitutes'][1]['id'])            
            json_element['player14_YC_h'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['substitutes'][2]['id'])            
            json_element['player15_YC_h'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['substitutes'][3]['id'])            
            json_element['player16_YC_h'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['substitutes'][4]['id'])            
            json_element['player17_YC_h'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['substitutes'][5]['id'])  if (len(get_dtls(lineup1['teamLists'],t_h_id)['substitutes'])>5 ) else 0                      
            json_element['player18_YC_h'] =  get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_h_id)['substitutes'][6]['id']) if (len(get_dtls(lineup1['teamLists'],t_h_id)['substitutes'])>6 ) else 0            
            json_element['player1_YC_a'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['lineup'][0]['id'])            
            json_element['player2_YC_a'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['lineup'][1]['id'])            
            json_element['player3_YC_a'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['lineup'][2]['id'])            
            json_element['player4_YC_a'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['lineup'][3]['id'])            
            json_element['player5_YC_a'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['lineup'][4]['id'])            
            json_element['player6_YC_a'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['lineup'][5]['id'])            
            json_element['player7_YC_a'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['lineup'][6]['id'])            
            json_element['player8_YC_a'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['lineup'][7]['id'])            
            json_element['player9_YC_a'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['lineup'][8]['id'])            
            json_element['player10_YC_a'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['lineup'][9]['id'])            
            json_element['player11_YC_a'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['lineup'][10]['id']) if (len(get_dtls(lineup1['teamLists'],t_a_id)['lineup'])>10 ) else 0              
            json_element['player12_YC_a'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['substitutes'][0]['id'])            
            json_element['player13_YC_a'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['substitutes'][1]['id'])            
            json_element['player14_YC_a'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['substitutes'][2]['id'])            
            json_element['player15_YC_a'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['substitutes'][3]['id'])            
            json_element['player16_YC_a'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['substitutes'][4]['id'])            
            json_element['player17_YC_a'] = get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['substitutes'][5]['id'])  if (len(get_dtls(lineup1['teamLists'],t_a_id)['substitutes'])>5 ) else 0                          
            json_element['player18_YC_a'] =  get_yc_count(lineup1['events'],get_dtls(lineup1['teamLists'],t_a_id)['substitutes'][6]['id']) if (len(get_dtls(lineup1['teamLists'],t_a_id)['substitutes'])>6 ) else 0                
            new_json[i].append(json_element)
            i=i+1

f=open(data,'a')
f.write(json.dumps(new_json,indent=1))
