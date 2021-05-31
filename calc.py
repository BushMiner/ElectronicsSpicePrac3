def avg(ls:list):
    return sum(ls)/len(ls)

tut_tests = avg([0,0,0.5,0.25,0.5,0])
tuts = avg([1,1,0,1,1])
prac_demo = avg([1,1])
prac_report = avg([1,0.5])

prac_3  = 0.666666




weights = [0.2,0.3,0.5]

sm = ((tut_tests+tuts+prac_demo+prac_report)*(1/6) + prac_3*(2/6))*100

a1 = 55



a2 = (50 - (sm*weights[0]+a1*weights[1]))/weights[2]


fm = sm*weights[0]+a1*weights[1]+a2*weights[2]

print(a2)



