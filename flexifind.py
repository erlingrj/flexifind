from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib import request
from dest_list import all_dest
import progressbar

class Flexifind:
    """ Example of format:
    origin: "Turin"
    dep_date: ("Monday", 5, "November", 2018)
    ret_date: ("Friday", 9, "November", 2018) 
    """
    def __init__(self, origin, dep_date, ret_date):
        self.origin = origin
        self.dep_date = dep_date
        self.ret_date = ret_date

        self.all_dest = all_dest
        opt = Options()
        opt.add_argument('--headless')
        self.driver = webdriver.Chrome(options = opt)
        self.driver.get("https://shop.flixbus.com/")    


    def change_origin(self, origin):
        self.origin = origin
    
    def change_dep_date(self, dep_date):
        self.dep_date = dep_date
    
    def change_ret_date(self, ret_date):
        self.ret_date = ret_date
    
    def type_origin(self):
        self.driver.find_element_by_class_name("lbhPck").find_element_by_tag_name("input").send_keys("{}\n".format(self.origin))

    def type_destination(self, dest):
        dest_input =self.driver.find_element_by_class_name("hepVrA").find_element_by_tag_name("input")
        dest_input.clear()
        dest_input.send_keys("{}\n".format(dest))

    
    def press_search_button(self):
        self.driver.find_element_by_class_name("ewlETO").click()

    def type_departure_date(self):
        (weekday,day,month,year) = self.dep_date
        search_string = "{}, {} {} {}".format(weekday,day,month,year)
        self.driver.find_element_by_class_name("dTvCQR").click()
        self.driver.find_element_by_class_name("iYKASO").find_element_by_xpath("//div[contains(@aria-label,'{}')]".format(search_string)).click()

    def type_return_date(self):
        (weekday,day,month,year) = self.ret_date
        self.driver.find_element_by_class_name("krLaRO").click()
        search_string = "{}, {} {} {}".format(weekday,day,month,year)
        self.driver.find_element_by_class_name("dTvCQR").click()
        self.driver.find_element_by_class_name("iYKASO").find_element_by_xpath("//div[contains(@aria-label,'{}')]".format(search_string)).click()

    def sort_results(self):
         self.driver.find_element_by_class_name("container-fluid").find_element_by_xpath("//option[contains(@value,'price')]").click()

    def get_best_price(self):
        go_price =  float(self.driver.find_element_by_xpath("//div[contains(@data-transport-type, 'bus') and contains(@data-group, 'direct')]").text.split('$')[1])
        ret_price = float(self.driver.find_element_by_xpath("//div[contains(@data-transport-type, 'bus') and contains(@data-group, 'return')]").text.split('$')[1])
        return go_price + ret_price
    
    def print_results(self, results):
            results.sort(key = lambda tup : tup[0])
            print("Prices from {}\n {} {} of {} {} - {} {} of {} {}".format(self.origin, self.dep_date[0],self.dep_date[1],self.dep_date[2],self.dep_date[3],self.ret_date[0],self.ret_date[1],self.ret_date[2],self.ret_date[3]))
            for res in results:
                print("{}: {}$".format(res[1],res[0]))


    def search_all_destination(self):
        self.type_origin()
        self.type_departure_date()
        self.type_return_date()

        results = []

        bar = progressbar.ProgressBar(maxval=len(self.all_dest), \
        widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()

        for idx, dest in enumerate(self.all_dest):
            self.type_destination(dest)
            try:
                self.press_search_button()
                self.sort_results()
                results.append((self.get_best_price(),dest))
            except:
                pass

            bar.update(idx)
        
        bar.finish()
        self.print_results(results)
    
    

    
def main():
    origin = "Turin"
    dep_date = ("Thursday",6,"December",2018)
    ret_date = ("Monday", 10, "December", 2018)

    f = Flexifind(origin, dep_date, ret_date)
    f.search_all_destination()

if __name__ == '__main__':
    main()

