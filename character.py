import random

def does_hit(hit):
    roll = random.randrange(100) + 1
    hit_chance = 83 + hit

    # capping of max hit chance to 99%
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

    def __init__(self, int, mana, damage, hit, crit, talents="00000", race="Gnome", name="player",dmf = False, five_dc = False):
        # TODO include damage modifier for buffs i.e. DMF buff
        self.int = int
        self.mana = mana
        self.dmg = damage
        self.hit = hit
        self.crit = crit + int / 60 + 2.5
        self.talents = talents
        self.race = race
        self.name = name
        self.cost_mod = 1 - five_dc * 0.15 # cost modifier for shadow bolt with 5-p doomcaller
        self.dmf = dmf # darkmoon faire buff

    def __str__(self):
        # gives a multiline infostring about the character's current stats
        talents = self.talents
        infostring = self.name.capitalize() + "   " + self.race + " Warlock" + "\
         \n*********************" + "\
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

    def sb(self, rank=10):
        """Requests Shadow bolt from player and returns the damage integer value and whether it crit and if Imp Sb is applied"""
        # TODO Create cast time and return based off warlock talents and rank
        # TODO Add functionality for all ranks of SB
        # check if spell hits ; i.e. ROLL 1
        is_hit = does_hit(self.hit)
        # check if spell crits ; i.e. ROLL 2
        is_crit = does_crit(self.crit)
        # (True/False parses as 1 or 0 and can successfully used in calculations)
        # depending on SB rank, gives different base values
        if rank == 9:
            randbase = random.randrange(455, 508)

            # calculates damage with different multipliers:
            # (BASE ROLL   +  DMG * COEFF) * CRIT MODIFIER, DEPENDANT ON RUIN or NOT * HIT CHECK * SM / DS modifier
            damage = (randbase + self.dmg / 3.5 * 3) * ((is_crit * (int(self.talents[2]) + 1) / 2) + 1) * is_hit

        else:
            randbase = random.randrange(482, 539)
            # SAME AS LINES 58-59
            damage = (randbase + self.dmg / 3.5 * 3) * is_hit * ((is_crit * (int(self.talents[2]) + 1) / 2) + 1)
        return damage, is_crit

    def cast_sb(self, target, rank=9):
        manacost = (25,40,70,110,160,210,265,363,370,380) #manacost list gives manacost depending on spell cast
        self.mana -= manacost[rank-1] * self.cost_mod # takes 5-p doomcaller into account
        sb = self.sb(rank) #original shadow damage, before target modifiers
        debuffs = target.debuffs
        sbdmg = sb[0]

        if "sw" in debuffs: # check for Shadow Weaving (sw)
            sbdmg *= 1.15
        if "nf" in debuffs: # check for Nightfall (nf)
            sbdmg *= 1.15
        if "cos" in debuffs: # check for Curse of Shadows (cos)
            sbdmg *= 1.10
        if target.imp_sb and sb[0]: # check for imp_sb and correct stacks where applicable
            target.imp_sb -= 1
            sbdmg *= 1.20
        if sb[1]*does_hit(self.hit): # checks for crits and rolls for the Imp Sb application
            target.imp_sb = 4
        return sbdmg

class Target:
    # TODO possibly add other resistances than shadow at a later point
    def __init__(self, sr, debuffs=[], imp_sb=0):
        """initialize the target to be damaged, will be a PVE target"""

        self.sr = sr  # Target Shadow resistance
        self.debuffs = debuffs  # all the debuffs currently on target, Imp SB counter will be tracked elsewhere
        self.imp_sb = imp_sb  # number of improved SB debuff stack currently on target, starts at 0

    def __str__(self):
        debuffs = ""
        for element in self.debuffs:
            debuffs = debuffs + element + " "
        infostring = "Shadow resistance: " + str(self.sr) + "\
        \nDebuffs: " + debuffs

        return infostring


def main():
    t = Target(50,["cos","sw","nf"])
    john = Warlock(300,5500,490,6,4,"01111","Gnome","Johonnie")
    print(t)
    print(john)
    for i in range(20):
        print(john.cast_sb(t,9))


if __name__ == "__main__":
    main()
