# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.

import logging
import time,random
import requests
import json
import pymysql
from bs4 import  BeautifulSoup as bs
import cn2an
import nums_from_string as nfs

def SalNum(i):
    ex = i
    ex1 = ex.replace(",", ".")
    ex2 = cn2an.transform(ex1)
    if "θ¬" in ex2:
        number = nfs.get_nums(ex2)
        Number=[]
        for i in number:
            num = i*10000
            Number.append(round(num))
        return Number
    else:
        Number=[]
        number = nfs.get_nums(ex2.replace(".", ""))
        for i in number:
            num = i
            Number.append(round(num))
        return Number

def ave(i):
    if len(i) == 2:
        num = 0
        for a in i:
            num = num+a
            Sal = round(num/2)
        return Sal
    else:
        Sal = round(i[0])
        return Sal

def annual(i):
    if i < 400000:
        return i*14
    else:
        return i

def main(ser:str) -> str:
    jdata=json.loads(ser)
    sp=jdata['search'].replace('γ','&term[]=')
    rp=jdata['page']

    logging.info('Yourator Start Search')

    db_settings = {
        "host": "azsqltop.mysql.database.azure.com",
        "port": 3306,
        "user": "jeff",
        "password": "@a0987399832",
    }
    conn = pymysql.connect(**db_settings)
    cursor = conn.cursor()
    
    for p in range(1,rp):
        res = requests.get("https://www.yourator.co/api/v2/jobs?term[]={}&sort=most_related&page={}".format(sp,p)).json()["jobs"]
        if res == []:
            break
        for n in range(len(res)):
            try:
                cursor.execute("insert career.newjob(id,job,location,lastupdate,company,annualsalary,salary,education,website) values('{}','{}','{}','{}','{}','{}','{}','δΈζ','yourator') on duplicate key update job=values(job),location=values(location),lastupdate=values(lastupdate),company=values(company),annualsalary=values(annualsalary),salary=values(salary),education=values(education),website=values(website);".format(res[n]["id"],res[n]["name"],res[n]["city"],res[n]["category"]["updated_at"],res[n]["company"]["brand"],annual(ave(SalNum(res[n]["salary"]))),res[n]["salary"]))
                conn.commit()
            except Exception:
                logging.info(str(p)+','+str(n))
            soup = bs(requests.get("https://www.yourator.co"+res[n]["path"]).text,'lxml')

            for i,e in enumerate(soup.select("h2.job-heading")):

                if e.text == "ε·₯δ½ε§ε?Ή":
                    try:
                        l=[t.text.replace("'","").replace("\n","γ") for t in soup.select("section.content__area")[i].select("li")]
                        if l == []:
                           l=[t.text.replace("'","").replace("\n","γ") for t in soup.select("section.content__area")[i].select("p")]
                        j=json.dumps(l,ensure_ascii=False)
                        cursor.execute("update career.newjob set description='{}' where id='{}';".format(j,res[n]["id"]))
                        conn.commit()
                    except Exception as m:
                        logging.info(str(p)+','+str(n)+','+str(res[n]["id"])+','+res[n]["name"]+','+e.text+','+str(m))

                if e.text == "ζ’δ»Άθ¦ζ±":
                    try:
                        l=[t.text.replace("'","").replace("\n","γ") for t in soup.select("section.content__area")[i].select("li")]
                        if l == []:
                            l=[t.text.replace("'","").replace("\n","γ") for t in soup.select("section.content__area")[i].select("p")]
                        j=json.dumps(l,ensure_ascii=False)
                        cursor.execute("update career.newjob set skill='{}' where id='{}';".format(j,res[n]["id"]))
                        conn.commit()
                    except Exception as m:
                        logging.info(str(p)+','+str(n)+','+str(res[n]["id"])+','+res[n]["name"]+','+e.text+','+str(m))

                # if e.text == "ε εζ’δ»Ά":
                #     try:
                #         l=[t.text.replace("'","").replace("\n","γ") for t in soup.select("section.content__area")[i].select("li")]
                #         if l == []:
                #             l=[t.text.replace("'","").replace("\n","γ") for t in soup.select("section.content__area")[i].select("p")]
                #         j=json.dumps(l,ensure_ascii=False)
                #         cursor.execute("update career.yourator set skilloption='{}' where id={};".format(j,res[n]["id"]))
                #         conn.commit()
                #     except Exception as m:
                #         logging.info(str(p)+','+str(n)+','+str(res[n]["id"])+','+res[n]["name"]+','+e.text+','+str(m))

                if e.text == "ε‘ε·₯η¦ε©":
                    try:
                        l=[t.text.replace("'","").replace("\n","γ") for t in soup.select("section.content__area")[i].select("li")]
                        if l == []:
                            l=[t.text.replace("'","").replace("\n","γ") for t in soup.select("section.content__area")[i].select("p")]
                        j=json.dumps(l,ensure_ascii=False)
                        cursor.execute("update career.newjob set benefits='{}' where id='{}';".format(j,res[n]["id"]))
                        conn.commit()
                    except Exception as m:
                        logging.info(str(p)+','+str(n)+','+str(res[n]["id"])+','+res[n]["name"]+','+e.text+','+str(m))
            time.sleep(random.uniform(2, 4))
        time.sleep(random.uniform(5, 8))
    cursor.close()
    conn.close()
    logging.info(f"ε·²ζ°ε’ {jdata['search']} θ·ηΌΊζ₯θ©’θ³ Yourator ({jdata['page']} ι ) !")

    return f"ε·²ζ°ε’ {jdata['search']} θ·ηΌΊζ₯θ©’θ³ Yourator ({jdata['page']} ι ) !"
