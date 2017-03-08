import random
import uuid

for nc in [10, 25, 50, 100]:
    for i in range(1, 26):
        target = open (str(nc) + "-cities-no-" + str(i), 'w')
        target.write("<%d>\n" % (nc))
        for _ in range(0, nc):
            cityid = uuid.uuid4()
            x = random.randint(0,100)
            y = random.randint(0,100)
            target.write("<%s> <%d> <%d>\n" % (cityid, x, y))
        target.close()
