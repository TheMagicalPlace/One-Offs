
from typing import List,Any
from random import randint

class Country:

    def __init__(self,country,
                 population: int,
                 wealth : str ,
                 humidity : str,
                 climate: str,
                 pop_density : str,
                 port : str = None,
                 airport : str = None,
                 land_borders : List[str] = None,):

        """ setting initial unique data for each country"""

        self.wealth = wealth; # wealthy, mixed, or poor
        self.humidity=humidity; # humid , mixed , or arid
        self.climate=climate; # hot , mixed , or cold
        self.pop_density=pop_density; # urban , mixed , rural
        self.port=port; # True or None
        self.airport = airport; # True or None
        self.land_borders = land_borders;
        self.healthy = population
        self.infected = 0
        self.dead = 0
        self.country_attributes = {'wealth':wealth,'pop_density':pop_density,'climate':climate,'humidity':humidity}

    def update_infected(self,virus):
        """how many new people are infected"""
        chance_of_meeting = randint(25,100)/100 # odds an infected person meets a non-infected one, fixed
        chance_of_infection = 0.1 # base, fixed
        chance_of_infection *= virus.infectivity # 1-10 , where ten is a 100 % chance of infection

        # country modifiers:
        for attribute,value in self.country_attributes.items():
            chance_of_infection += 0.1*virus.attributes[attribute][value] # virus infectivity in conditions, from -2,2

        if chance_of_infection > 1:
            new_infected = 2*self.infected*chance_of_meeting
        else:
            if chance_of_infection > 0:
                new_infected = int(chance_of_infection*self.infected*chance_of_meeting+0.75)
        if chance_of_infection < 0 :
            return
        elif self.infected + new_infected > self.dead+self.healthy:
            self.infected += self.healthy
            self.healthy = 0
        else:
            self.infected += int(new_infected)
            self.healthy -= int(new_infected)


class Disease:
    """super-class for pathogens"""

    def __init__(self,base_infectivity=0,base_severity=0,base_lethality=0,**modifiers):
        self.infectivity = base_infectivity
        self.severity = base_severity
        self.lethality = base_lethality

        self.attributes = {
        'wealth':{'rich':-2,'mixed':-1,'poor':0},
        'climate':{'hot':-2,'mixed':0,'cold':-2},
        'pop_density':{'urban':0,'mixed':-1,'rural':-2},
        'humidity':{'humid':-0.5,'mixed':0,'arid':-1}
        }

        for cat,mods in modifiers.items():
            for mod,value in mods.items():
                self.attributes[cat][mod] =value



if __name__ == '__main__':
    A = {'country':'A','population':100000,'wealth':'rich','climate':'mixed','pop_density':'mixed','humidity':'humid'}
    dis_mods = [1,0,0,{
        'wealth':{'rich':2,'mixed':1,'poor':1},
        'climate':{'hot':0,'mixed':0,'cold':0},
        'pop_density':{'urban':0,'mixed':0,'rural':0},
        'humidity':{'humid':0,'mixed':0,'arid':0}
        }]
    gen_dis = Disease(*dis_mods[:-1],**dis_mods[-1])
    gen_A = Country(**A)
    print(A)
    gen_A.infected = 1
    for i in range(100):
        gen_A.update_infected(gen_dis)
        print(gen_A.healthy,gen_A.infected,gen_A.dead)