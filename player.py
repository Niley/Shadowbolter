import random

def does_hit(hit):
    roll = random.randrange(100)+1
    hit_chance = 83 + hit

    #capping of max hit chance to 99%
    if hit_chance > 99:
        hit_chance = 99

    if roll < 83 + hit:
        return True
    return False

def does_crit(crit):
    roll = random.randrange(100) + 1

    if roll <= crit:
        return True
    return False

class Warlock:
    # talents string is a 5-char list indicating SM, DS, IMP SB, BANE and RUIN talents

    def __init__(self, int, mana, damage, hit, crit, talents="00000", race="Gnome", name="player"):

        self.int = int
        self.mana = mana
        self.dmg = damage
        self.hit = hit
        self.crit = crit + int/60 + 2.5
        self.talents = talents
        self.race = race
        self.name = name

    def __str__(self):
        #gives a multiline infostring about the character's current stats
        talents = self.talents
        infostring = self.name.capitalize() + "   " + self.race + " Warlock"  + "\
         \n*********************"+"\
         \nSpell damage:\t" + str(self.dmg) + "\
         \nSpell crit:\t\t" + str(self.crit) + "\
         \nSpell hit:\t\t" + str(self.hit) + "\
         \n\nTalents:" + "\
         \n\tShadow Mastery" * int(talents[0]) + "\
         \n\tDemonic Sacrifice" * int(talents[1]) + "\
         \n\tImproved Shadow Bolt" * int(talents[2]) + "\
         \n\tBane" * int(talents[3]) + "\
         \n\tRuin" * int(talents[4])

        return infostring

    def sb(self,rank = 10):
        """Requests Shadow bolt from player and returns the damage integer value and whether it crit and if Imp Sb is applied"""
        # TODO Create cast time and return base off warlock talents
        # TODO Add functionality for all ranks of SB
        # check if spell hits ; i.e. ROLL 1
        is_hit = does_hit(self.hit)

        # check if spell crits ; i.e. ROLL 2
        is_crit = does_crit(self.crit)
        # (True/False parses as 1 or 0 and can successfully used in calculations)

        # depending on SB rank, gives different base values
        if rank == 9:
            randbase = random.randrange(455,508)

            # calculates damage with different multipliers:
            # (BASE ROLL   +  DMG * COEFF) * CRIT MODIFIER, DEPENDANT ON RUIN or NOT * HIT CHECK * SM / DS modifier
            damage = (randbase + self.dmg/3.5*3)*((is_crit*(int(self.talents[2])+1)/2)+1)*is_hit

        else:
            randbase = random.randrange(482,539)
            # SAME AS LINES 58-59
            damage = (randbase + self.dmg/3.5*3) * is_hit * ((is_crit * (int(self.talents[2]) + 1) / 2) + 1)
        return int(damage),is_crit,(is_crit*is_hit)*does_hit(self.hit)

def main():
    john = Warlock(300, 6000, 500, 0, 20, "00000", "Gnome", "john")
    ben = Warlock(250, 5000, 500, 0, 20, "00100", "Human", "ben")
    print(ben)
    print("Shadowbolt does "+ str(ben.sb(9)) + " damage.")
    print(john)
    print("Shadowbolt does "+ str(john.sb(9)) + " damage.")


if __name__ == "__main__":
    main()