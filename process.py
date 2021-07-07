import json
import dateutil.parser
import statistics

path = './parsed-logs-35/undefined__143__1.0.0__2021-05-24-09-40-49/metrics.jsonl'

out_path = './data.json'

parameters = {}

with open(path) as f:
    lines = f.readlines()
    ids = []
    for line in lines:
        if line != None and line != "\n":
            line_acc = line.replace("'", "\"")
            d = json.loads(line)
            id = int(d.get("jobId").split('-')[2])
            ids.append(id)
            if id not in parameters:
                parameters[id] = {
                    "cpu": [],
                    "memory": [],
                    "ctime": [],
                    "io": [],
                    "network": [],
                    "timestamps": {
                        "handlerStart": None,
                        "handlerEnd": None,
                        "jobStart": None,
                        "jobEnd": None
                    }
                }

            if d.get("parameter") == "event":
                value = d.get("value")
                if parameters[id]["timestamps"][value] is None or d.get("time") < parameters[id]["timestamps"][value]:
                    parameters[id]["timestamps"][value] = d.get("time")
                else:
                    print(value + " To be" + d.get("time") + " Value! " + parameters[id]["timestamps"][value])
                # parameters[id]["timestamps"].append(d.get("value"))
            else:
                parameters[id][d.get("parameter")].append(d.get("value"))
                
            
    
    #print(json.dumps(parameters[1], indent=2))
    ids.sort()
    #print(set(ids))

with open(out_path, 'w+') as f:
    d_out = {}
    for key in parameters:
        in_dir  = {
            'time': None,
            'cpu': None
        }

        date1 = dateutil.parser.parse(parameters[key]['timestamps']["handlerStart"])
        date2 = dateutil.parser.parse(parameters[key]['timestamps']["handlerEnd"])

        in_dir['time'] = (date2 - date1).total_seconds()
        in_dir['cpu'] = sum(parameters[key]['cpu']) / len(parameters[key]['cpu']) if sum(parameters[key]['cpu']) / len(parameters[key]['cpu']) > 0 else 0.5
        #in_dir['cpu_list'] = parameters[key]['cpu']
        #in_dir['memory'] = sum(parameters[key]['memory']) / len(parameters[key]['memory']) #if len(parameters[key]['memory']) > 0 else 0
        
        d_out[key] = in_dir

    json.dump(d_out, f, indent=4)
