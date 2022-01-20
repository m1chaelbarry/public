from faker import Faker
from faker.providers import person, internet, misc
import os, re, time
import http.client

Mailsac_Api_Key = 'API-KEY-HERE' #  <<<<<<<<<<<<<<ADD KEY HERE!!!

fake = Faker()
gen_email = fake.lexify(text='??????????@mailsac.com')
gen_name = fake.name()
gen_password = fake.password(length=12)

def registerAcc(email, name, password):
    stream = os.popen(f'megatools reg --scripted --register --email {email} --name {name} --password {password}')
    output = stream.read()
    return(output) 

def GetEmailID(email):
    conn = http.client.HTTPSConnection("mailsac.com")
    headersList = {
    "Mailsac-Key": Mailsac_Api_Key 
    }
    payload = ""
    # print(f'checking email: {email}')
    conn.request("GET", f"/api/addresses/{email}/messages", payload, headersList)
    response = conn.getresponse()
    result = response.read().decode("utf-8")
    extracted_id = str(re.findall('(?<="_id":").[^"]+', result))
    extracted_id = str(extracted_id[2:-2])
    # print(extracted_id)
    if len(extracted_id) == 0:
        time.sleep(5)
        GetEmailID(email)
    
    return(extracted_id)

def GetEmailContentFromID(email, id):
    _id = id

    conn = http.client.HTTPSConnection("mailsac.com")

    headersList = {
    "Mailsac-Key": Mailsac_Api_Key 
    }
    payload = ""
    conn.request("GET", f'/api/text/{email}/{_id}', payload, headersList)
    response = conn.getresponse()
    result = response.read()
    return(result.decode("utf-8"))

def ExtractURL(url):
    return(re.search("(?P<url>https?://[^\s]+)", url).group("url"))

def VerifyAcc(command, link):
    verify_command = command.replace("@LINK@", link)
    # print(verify_command)
    stream = os.popen(verify_command)
    output = stream.read()
    return(output) 

def register():
    # print(f"email: {gen_email}, name: {gen_name}, password: {gen_password}.")  
    verify = registerAcc(gen_email, gen_name, gen_password)
    GetEmailID(gen_email)
    link = (ExtractURL(GetEmailContentFromID(gen_email, GetEmailID(gen_email))))
    # print(verify)
    # print(link)
    VerifyAcc(verify, link)
    Credentials = [gen_email, gen_password]
    return(Credentials)

def AppendToFile():
    register()
    readable = f'{gen_email}:{gen_password}\n'
    print(readable)
    file_object = open('creds.txt', 'a')
    file_object.write(readable)
    file_object.close()
    


if __name__ == "__main__":
    AppendToFile()