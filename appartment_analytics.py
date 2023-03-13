import pandas as pd

# row example ["Professorsslingan 35 / 1302",[1,156,427,547,558,547,740],"https://sssb.se/soka-bostad/sok-ledigt/lediga-bostader/lagenhet/?refid=42486935644c424b5872656951676a5168393149337074755a51445358443568","3 rum \u0026 pentry"],
def analyze(rows):
    # create a dataframe for each unique appartment type at each unique address, ignoring the address number (i.e. 3 rum & pentry at Professorsslingan)
    unique_appartments = {}
    for row in rows:
        # remove numbers from address eg. Professorsslingan 35 / 1302 -> Professorsslingan
        index = 0
        for char in row[0]:
            if char.isdigit():
                break
            index += 1
        address = row[0][:index].strip()
        type_app = row[3]
        last_day = row[1][-1]
        # if nan, skip
        
        # if dataframe for this appartment type at this address does not exist, create it
        if (address, type_app) not in unique_appartments:
            unique_appartments[(address, type_app)] = pd.DataFrame(
                columns=["address", "type", "dagar"]
            )
        else: # if it does exist, append the last day to the dataframe
            # use concat instead of append to avoid the warning
            unique_appartments[(address, type_app)] = pd.concat(
                [
                    unique_appartments[(address, type_app)],
                    pd.DataFrame(
                        [[address, type_app, last_day]], columns=["address", "type", "dagar"]
                    ),
                ]
            )

    
    # group by addresses
    # Professorslingan
    # Professorslingan Korridor 532 300
    # Professorslingan 1 rum & kök  532 301
    addresses = {}
    for key in unique_appartments:

        avg = (unique_appartments[key]["dagar"].mean())
        # if average is nan, print the dataframe
        if pd.isna(avg):
            continue
        avg = round(avg)
        datapoints = len(unique_appartments[key])
        if key[0] not in addresses:
            addresses[key[0]] = []
        addresses[key[0]].append((key[1], avg, datapoints))
    # convert to list
    avg_results = []
    for address in addresses:
        avg_results.append((address, addresses[address]))

    
        
        
    return avg_results

