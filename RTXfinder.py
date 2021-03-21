#https://www.bestbuy.ca/ns/mobile/android/configuration/v1.3.0/en

import requests, json, codecs, win10toast, time, concurrent.futures, webbrowser

start = time.time()

#this must be reset after every notification (prevents spam). It will automatically reset after 5 minutes.
notified = False

webCode = "15166285"
#RTX 3070: 15078017 
#RTX 3060 Ti: 15166285

#if prerelease is true, RTXfinder will only check for preorders and preorder detail updates
#if prerelease is false, RTXfinder will only check for immediately buyable stock
prerelease = True

#if pageFounds is false, RTXfinder will only check for search results
pageFound = True
searchTerm = "RTX 3060"

#create an object for the notification
from win10toast import ToastNotifier
notification = ToastNotifier()

#used to open the product page when notification is clicked
def urlOpen():
    webbrowser.open("https://www.bestbuy.ca/en-ca/product/nvidia-geforce-rtx-3060-ti-8gb-gddr6-video-card/15166285")

#checks the product details
def productChecker():
    global notified
    global notification
    global prerelease
    #pulls product info
    response = requests.get('https://www.bestbuy.ca/api/v2/json/product/'+webCode, headers=headers)
    if response.ok:
        json1 = response.json()
        if prerelease:
            #checks if item is preorderable
            if json1["isPreorderable"]:
                notification.show_toast("RTX 3060 Ti IN STOCK","Available for preorder now!", threaded=True, callback_on_click=urlOpen)
                notified = True
            #checks if item is purchasable
            if json1["isPurchasable"]:
                notification.show_toast("RTX 3060 Ti IN STOCK","Available for preorder now!", threaded=True, callback_on_click=urlOpen)
                notified = True
            #checks if preorder date is added
            elif json1["PreorderOrderDate"]!="":
                notification.show_toast("RTX 3060 Ti UPDATE","Preorder date is "+json1["PreorderOrderDate"], threaded=True, callback_on_click=urlOpen)
                notified = True
            # checks if item preorder release date is updated
            elif json1["PreorderReleaseDate"]!="":
                notification.show_toast("RTX 3060 Ti UPDATE","Preorder release date is "+json1["PreorderReleaseDate"], threaded=True, callback_on_click=urlOpen)
                notified = True
            elif json1["isProductOnSale"]:
                notification.show_toast("RTX 3060 Ti IN STOCK","Unknown stock levels", threaded=True, callback_on_click=urlOpen)
                notified = True
        else:
            if json1["isProductOnSale"]:
                notification.show_toast("RTX 3060 Ti IN STOCK","Unknown stock levels", threaded=True, callback_on_click=urlOpen)
                notified = True
            elif json1["isBackorderable"]:
                notification.show_toast("RTX 3060 Ti IN STOCK","Available for backorder", threaded=True, callback_on_click=urlOpen)
                notified = True
    else:
        notification.show_toast("ERROR","Product page not found", threaded=True, callback_on_click=urlOpen)
        notified = True

#checks product availability info
def availabilityChecker():
    global notified
    global notification
    #pulls product availability
    response = requests.get('https://www.bestbuy.ca/ecomm-api/availability/products?accept=application%2Fvnd.bestbuy.standardproduct.v1%2Bjson&skus='+webCode, headers=headers)
    if response.ok:
        data=codecs.decode(response.text.encode(), 'utf-8-sig')
        json2 = json.loads(data)
        if json2["availabilities"][0]["shipping"]["status"]!="ComingSoon":
            notification.show_toast("RTX 3060 Ti IN STOCK",str(json2["availabilities"][0]["shipping"]["quantityRemaining"])+" units left", threaded=True, callback_on_click=urlOpen)
            notified = True
        elif json2["availabilities"][0]["shipping"]["purchasable"]==True:
            notification.show_toast("RTX 3060 Ti IN STOCK",str(json2["availabilities"][0]["shipping"]["quantityRemaining"])+" units left", threaded=True, callback_on_click=urlOpen)
            notified = True
        elif json2["availabilities"][0]["shipping"]["isBackorderable"]==True:
            notification.show_toast("RTX 3060 Ti IN STOCK", "Available for backorder", threaded=True, callback_on_click=urlOpen)
            notified = True

#checks search results
def searchChecker():
    global pageFound
    global webCode
    global notification
    response = requests.get('https://www.bestbuy.ca/api/v2/json/search?categoryid=&query=rtx%203060&exp=&sortBy=relevance&sortDir=desc', headers=headers)
    if response.ok:
        data=codecs.decode(response.text.encode(), 'utf-8-sig')
        json3 = json.loads(data)
        if json3["products"]:
            notification.show_toast("RTX 3060 Ti UPDATE", str(len(json3["products"]))+" listings found!", threaded=True, callback_on_click=urlOpen)
            webCode = str(json3["products"][0]["sku"])
            pageFound = True
#headers to fake browser
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',}

if __name__ == "__main__":
    while True:
        #swap between ThreadPoolExecutor and ProcessPoolExecutor to swap between multiprocessing and multithreading
        with concurrent.futures.ThreadPoolExecutor() as executor:
            if notified is False:
                if pageFound:
                    #creates parallel processes
                    processes = [executor.submit(productChecker), executor.submit(availabilityChecker)]
                    productChecker()
                    availabilityChecker()
                else:
                    searchChecker()
            #waits a set amount of time before sending another notification
            else:
                #change the number below to set the interval between notifications (in seconds)
                time.sleep(300)
                notified = False