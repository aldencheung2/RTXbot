#scrapes listings for new graphics cards

import requests, codecs, win10toast, time, concurrent.futures, os

#headers to fake browser 
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',}
#starting webCode
webCode = 14902000

#create an object for the notification
from win10toast import ToastNotifier
notification = ToastNotifier()

#stores the number of results
resultsFound = 0

start=time.time()

#checks the webCode and writes to file if the webCode is of interest
def webcodeChecker(webCode):
    #pulls product info
    response = requests.get('https://www.bestbuy.ca/api/v2/json/product/'+str(webCode), headers=headers)
    #converts to JSON
    json = response.json()
    global resultsFound
    #checks if the product does not exist
    if json is not None:
        if json["categoryName"] == "Graphics Cards":
            file.write(json["seoText"]+": "+json["sku"]+"\n")
            resultsFound+=1
            return "found"
        if json["isVisible"] is False:
            file.write(json["seoText"]+": "+json["sku"]+"\n")
            resultsFound+=1
            return "found"
        if json["manufacturer"] == "NVID":
            file.write(json["seoText"]+": "+json["sku"]+"\n")
            resultsFound+=1
            return "found"

#number of processes or threads
threadCount = 100

file = open("scrapingResults.txt", "w")

#runs function in parallel
if __name__ == "__main__":
    while True:
        #stops checking if webcode exceeds 180000000 and notifies user
        if webCode>180000000:
            notification.show_toast("Scraping complete",str(resultsFound)+" results found!")
            file.write("Final SKU: "+str(webCode))
            break

        #swap between ThreadPoolExecutor and ProcessPoolExecutor to swap between multiprocessing and multithreading
        with concurrent.futures.ThreadPoolExecutor() as executor:
            #creates parallel processes
            processes = [executor.submit(webcodeChecker, webCode+i) for i in range(threadCount)]

            #prints the outputs of the processes
            for item in concurrent.futures.as_completed(processes):
                if item.result() != None:
                    print(item.result())

        #notifies user of current progress every 10000 items
        if webCode%1000==0:
            print(str(time.time()-start)+"s: currently processing "+str(webCode))
        webCode+=threadCount
        
        file.flush()
        os.fsync(file)


#used for performance testing
#print(time.time()-start)

file.close()