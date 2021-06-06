import json
import dateutil.parser
import statistics

path = './parsed-logs/tmp/job_descriptions.jsonl'
out_path = './file_sizes.json'

f_sizes = {}

with open(path) as f:
    lines = f.readlines()
    ids = []
    for line in lines:
        if line != None and line != "\n":
            line_acc = line.replace("'", "\"")
            #print(line)
            d = json.loads(line)
            if "inputs" in d:
                for file in d["inputs"]:
                    if file["name"] not in f_sizes:
                        f_sizes[file["name"]] = file["size"]
                    #f_sizes[file["name"]].append(file["size"])
            
            if "outputs" in d:
                for file in d["outputs"]:
                    if file["name"] not in f_sizes:
                        f_sizes[file["name"]] = file["size"]
                    #f_sizes[file["name"]].append(file["size"])
                            
    #print(json.dumps(f_sizes, indent=2))

with open(out_path, 'w+') as f:
    json.dump(f_sizes, f, indent=2)