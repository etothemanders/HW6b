#!/usr/bin/env python
import robots
import sys

class Melon(object):

    def __init__(self, melon_type):
        self.melon_type = melon_type
        self.weight = 0.0
        self.color = None
        self.stickers = []

    def prep(self):
        robots.cleanerbot.clean(self)
        robots.stickerbot.apply_logo(self)
    
    def __str__(self):
        if self.weight <= 0:
            return self.melon_type
        else:
            return "%s %0.2fLB %s" % (self.color, self.weight, self.melon_type)
    

# 1. Create a new class WinterSquash, that inherits from Melon
# 2. Overwrite the WinterSquash prep method to include calling 
#    the painterbot's paint method
# 3. In main(), create a product dictionary, with the melon type as keys, and
#    the appropriate constructor as the value

class WinterSquash(Melon):
    
    def prep(self):
        robots.cleanerbot.clean(self)
        robots.stickerbot.apply_logo(self)
        robots.painterbot.paint(self)

def main():
    f = open("standing_orders2.log")
    
    products = {
        "Watermelon" : Melon("Watermeon"),
        "Honeydew": Melon("Honeydew"),
        "Musk Melon": Melon("Musk Melon"),
        "Winter Squash": WinterSquash("Winter Squash")
    }
    

    for line in f:
        (melon_type, quantity) = line.rstrip().split(':')
        quantity = int(quantity)
        
        count = 0
        melons = []
        while len(melons) < quantity:
            if count > 200:
                print "\nALL MELONS HAVE BEEN PICKED"
                print "ORDERS FAILED TO BE FULFILLED!"
                sys.exit()
            
            #m = Melon(melon_type)
            m = products[melon_type]
            robots.pickerbot.pick(m)
            count += 1
            
            m.prep()
            
            # evaluate melon
            presentable = robots.inspectorbot.evaluate(m)
            if presentable:
                melons.append(m)
            else:
                robots.trashbot.trash(m)
                continue

        print "------"
        print "Robots Picked %d %s for order of %d" % (count, melon_type, quantity)

        # Pack the melons for shipping
        boxes = robots.packerbot.pack(melons)
        # Ship the boxes
        robots.shipperbot.ship(boxes)
        print "------\n"


if __name__ == "__main__":
    main()
