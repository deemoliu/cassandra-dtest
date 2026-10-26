class Attack:
    def __init__(self, damage, type, weakness):
        self.damage = damage
        self.type = type
        self.weakness = weakness


class Monster:
    def __init__(self, name, health, type, weakness, attacks, defense=0):
        self.name = name
        self.health = health
        self.type = type
        self.weakness = weakness
        self.attacks = attacks
        self.defense = defense

class Team:
    def __init__(self, label, monsters):
        self.label = label
        self.monsters = monsters
        self.activeIdx = 0

    def getActive(self):
        if self.activeIdx < len(self.monsters):
            return self.monsters[self.activeIdx]
        return None

    def advanceAndNextLabel(self):
        self.activeIdx = self.activeIdx + 1
        if self.activeIdx < len(self.monsters):
            return self.label + ":" + self.monsters[self.activeIdx].name
        return "NONE"

    def hasAlive(self):
        return self.activeIdx < len(self.monsters)

"""
(1)modify the simulation to support asynchronous turns or parallel processing
(2)What architectural changes would allow for battle replay or move undo functionality?
(3)How would you efficiently handle complex monster abilities like buffs, debuffs, or AoE effects without degrading performance?
(4)How would you adapt this simulation if damage rules became context-dependent or changed dynamically mid-battle?
(5)What strategies would you use to minimize memory allocation when generating thousands of event strings?
(6)Could this turn-based flow be refactored into an event-driven architecture for better scalability?
"""

class Solution:
    def getHighestDamage(self, attacker, defender):
        highest = 0
        for attack in attacker.attacks:
            damage = (attack.damage * 2 if attack.type in defender.weakness
                      else attack.damage // 2 if defender.type in attack.weakness
                      else attack.damage)
            highest = max(highest, damage - defender.defense, 1)
        return highest

    def simulateBattle(self, teamA, teamB):
        log = ""
        ## ## round terminate when ativeA/ActiveB = len(teamA)
        while teamA.hasAlive() and teamB.hasAlive():
            ## A attack B first, update B's HP and log
            attacker = teamA.getActive()
            defender = teamB.getActive()
            ## stalemate: neither side can hurt the other, so the loop would never end
            if self.getHighestDamage(attacker, defender) == 0 and self.getHighestDamage(defender, attacker) == 0:
                log+=("[RESULT] DRAW\n")
                return log
            hpBefore = defender.health
            damage = self.getHighestDamage(attacker, defender)
            hpAfter = max(defender.health - damage, 0)
            log+=(f"[ATTACK] A:{attacker.name} -> B:{defender.name} | DMG={damage} | HP:{hpBefore} -> {hpAfter}\n")
            defender.health = hpAfter
            
            if hpAfter == 0:
                ## B death check, if dead activeB++, end the round
                next = teamB.advanceAndNextLabel()
                log+=(f"[DEATH] B:{defender.name} defeated | NEXT={next}\n")
                
            else:
                ## B death check, if not dead, B counterback, update A's HP and log
                hpBeforeA = attacker.health
                damage = self.getHighestDamage(defender, attacker)
                hpAfterA = max(attacker.health - damage, 0)
                log+=(f"[ATTACK] B:{defender.name} -> A:{attacker.name} | DMG={damage} | HP:{hpBeforeA} -> {hpAfterA}\n")
                attacker.health = hpAfterA
                if hpAfterA <= 0:
                    ## A death check, if dead activeA++, end the round
                    next = teamA.advanceAndNextLabel()
                    log+=(f"[DEATH] A:{attacker.name} defeated | NEXT={next}\n")

        winner = "A" if teamA.hasAlive() else "B"
        log+=(f"[RESULT] WINNER={winner}\n")
        return log

def assertLog(log, expected):
    actual = log.splitlines()
    assert actual == expected, "\nExpected:\n" + "\n".join(expected) + "\nActual:\n" + "\n".join(actual)
    print("PASS\n")

def test1():
    print("===== Test 1 =====")

    water = Attack(8, "Water", ["Electric"])
    grass = Attack(40, "Grass", ["Fire"])
    fire = Attack(5, "Fire", ["Water"])

    chimera = Monster("Chimera", 20, "Normal", [], [water, grass])
    flare = Monster("Flare", 18, "Fire", ["Water"], [fire])

    teamA = Team("A", [chimera])
    teamB = Team("B", [flare])

    log = Solution().simulateBattle(teamA, teamB)
    print(log)
    expected = [
        "[ATTACK] A:Chimera -> B:Flare | DMG=20 | HP:18 -> 0",
        "[DEATH] B:Flare defeated | NEXT=NONE",
        "[RESULT] WINNER=A"
    ]
    assertLog(log, expected)


def test2():
    print("===== Test 2 =====")

    fire = Attack(7, "Fire", ["Water"])
    normal = Attack(10, "Normal", [])
    grass = Attack(4, "Grass", ["Fire"])
    water = Attack(6, "Water", ["Electric"])
    electric = Attack(4, "Electric", ["Grass"])

    blaze = Monster("Blaze", 15, "Fire", ["Water"], [fire, normal])
    sprout = Monster("Sprout", 12, "Grass", ["Fire"], [grass])
    wave = Monster("Wave", 18, "Water", ["Electric"], [water, electric])

    teamA = Team("A", [blaze])
    teamB = Team("B", [sprout, wave])

    log = Solution().simulateBattle(teamA, teamB)
    print(log)
    expected = [
        "[ATTACK] A:Blaze -> B:Sprout | DMG=14 | HP:12 -> 0",
        "[DEATH] B:Sprout defeated | NEXT=B:Wave",
        "[ATTACK] A:Blaze -> B:Wave | DMG=10 | HP:18 -> 8",
        "[ATTACK] B:Wave -> A:Blaze | DMG=12 | HP:15 -> 3",
        "[ATTACK] A:Blaze -> B:Wave | DMG=10 | HP:8 -> 0",
        "[DEATH] B:Wave defeated | NEXT=NONE",
        "[RESULT] WINNER=A"
    ]
    assertLog(log, expected)


def test3():
    print("===== Test 3 =====")

    normal = Attack(6, "Normal", [])
    water = Attack(5, "Water", ["Electric"])
    fire = Attack(7, "Fire", ["Water"])
    grass = Attack(16, "Grass", ["Fire"])
    mageWater = Attack(6, "Water", ["Electric"])

    knight = Monster("Knight", 9, "Normal", ["Fire"], [normal, water])
    mage = Monster("Mage", 8, "Water", ["Electric"], [mageWater])
    pyre = Monster("Pyre", 20, "Fire", ["Water"], [fire, grass])

    teamA = Team("A", [knight, mage])
    teamB = Team("B", [pyre])

    log = Solution().simulateBattle(teamA, teamB)
    print(log)
    expected = [
        "[ATTACK] A:Knight -> B:Pyre | DMG=10 | HP:20 -> 10",
        "[ATTACK] B:Pyre -> A:Knight | DMG=16 | HP:9 -> 0",
        "[DEATH] A:Knight defeated | NEXT=A:Mage",
        "[ATTACK] A:Mage -> B:Pyre | DMG=12 | HP:10 -> 0",
        "[DEATH] B:Pyre defeated | NEXT=NONE",
        "[RESULT] WINNER=A"
    ]
    assertLog(log, expected)


def test4():
    print("===== Test 4 =====")

    fire = Attack(5, "Fire", ["Water"])
    water = Attack(9, "Water", ["Electric"])
    normal = Attack(7, "Normal", [])
    weakHit = Attack(2, "Normal", [])

    titan = Monster("Titan", 20, "Normal", [], [fire, water, normal])
    dummy = Monster("Dummy", 8, "Normal", [], [weakHit])

    teamA = Team("A", [titan])
    teamB = Team("B", [dummy])

    log = Solution().simulateBattle(teamA, teamB)
    print(log)
    expected = [
        "[ATTACK] A:Titan -> B:Dummy | DMG=9 | HP:8 -> 0",
        "[DEATH] B:Dummy defeated | NEXT=NONE",
        "[RESULT] WINNER=A"
    ]
    assertLog(log, expected)


def test5():
    print("===== Test 5 =====")

    electric = Attack(6, "Electric", ["Grass"])
    fire = Attack(8, "Fire", ["Water"])
    water = Attack(5, "Water", ["Electric"])
    grass = Attack(9, "Grass", ["Fire"])
    leafGrass = Attack(5, "Grass", ["Fire"])
    leafNormal = Attack(7, "Normal", [])
    rockNormal = Attack(8, "Normal", [])
    rockElectric = Attack(6, "Electric", ["Grass"])

    bolt = Monster("Bolt", 10, "Electric", ["Grass"], [electric, fire])
    aqua = Monster("Aqua", 12, "Water", ["Electric"], [water, grass])
    leaf = Monster("Leaf", 11, "Grass", ["Fire"], [leafGrass, leafNormal])
    rock = Monster("Rock", 20, "Normal", ["Water"], [rockNormal, rockElectric])

    teamA = Team("A", [bolt, aqua])
    teamB = Team("B", [leaf, rock])

    log = Solution().simulateBattle(teamA, teamB)
    print(log)
    expected = [
        "[ATTACK] A:Bolt -> B:Leaf | DMG=16 | HP:11 -> 0",
        "[DEATH] B:Leaf defeated | NEXT=B:Rock",
        "[ATTACK] A:Bolt -> B:Rock | DMG=8 | HP:20 -> 12",
        "[ATTACK] B:Rock -> A:Bolt | DMG=8 | HP:10 -> 2",
        "[ATTACK] A:Bolt -> B:Rock | DMG=8 | HP:12 -> 4",
        "[ATTACK] B:Rock -> A:Bolt | DMG=8 | HP:2 -> 0",
        "[DEATH] A:Bolt defeated | NEXT=A:Aqua",
        "[ATTACK] A:Aqua -> B:Rock | DMG=10 | HP:4 -> 0",
        "[DEATH] B:Rock defeated | NEXT=NONE",
        "[RESULT] WINNER=A"
    ]
    assertLog(log, expected)


def test6():
    print("===== Test 6 =====")

    strike = Attack(5, "Normal", [])

    guardian = Monster("Guardian", 20, "Normal", [], [strike])

    teamA = Team("A", [guardian])
    teamB = Team("B", [])

    log = Solution().simulateBattle(teamA, teamB)
    print(log)
    expected = [
        "[RESULT] WINNER=A"
    ]
    assertLog(log, expected)


def test7():
    print("===== Test 7 =====")

    wallA = Monster("WallA", 20, "Normal", [], [])
    wallB = Monster("WallB", 20, "Normal", [], [])

    teamA = Team("A", [wallA])
    teamB = Team("B", [wallB])

    log = Solution().simulateBattle(teamA, teamB)
    print(log)
    expected = [
        "[RESULT] DRAW"
    ]
    assertLog(log, expected)


def test8():
    print("===== Test 8 =====")

    tap = Attack(3, "Normal", [])
    slam = Attack(10, "Normal", [])

    brute = Monster("Brute", 10, "Normal", [], [slam], defense=5)
    wall = Monster("Wall", 12, "Normal", [], [tap], defense=5)

    teamA = Team("A", [wall])
    teamB = Team("B", [brute])

    log = Solution().simulateBattle(teamA, teamB)
    print(log)
    expected = [
        "[ATTACK] A:Wall -> B:Brute | DMG=1 | HP:10 -> 9",
        "[ATTACK] B:Brute -> A:Wall | DMG=5 | HP:12 -> 7",
        "[ATTACK] A:Wall -> B:Brute | DMG=1 | HP:9 -> 8",
        "[ATTACK] B:Brute -> A:Wall | DMG=5 | HP:7 -> 2",
        "[ATTACK] A:Wall -> B:Brute | DMG=1 | HP:8 -> 7",
        "[ATTACK] B:Brute -> A:Wall | DMG=5 | HP:2 -> 0",
        "[DEATH] A:Wall defeated | NEXT=NONE",
        "[RESULT] WINNER=B"
    ]
    assertLog(log, expected)


if __name__ == "__main__":
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()
    test8()