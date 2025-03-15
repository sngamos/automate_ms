import math

def calculate_final_cd(original_skill_cd, cdr_percent, cdr_potential):
    if cdr_percent <1:
        cdr_percent*=100
    after_cdr_percent = original_skill_cd * (1 - cdr_percent/100)
    #print(after_cdr_percent)
    remaining_cdr=cdr_potential 
    if after_cdr_percent >10:
        above_10_cd = after_cdr_percent - 10
        if above_10_cd > cdr_potential:
            return round(10+ above_10_cd - cdr_potential,4)
        else:
            remaining_cdr = cdr_potential - above_10_cd

    percent_reduce = (remaining_cdr/0.01)*0.05/100
    #print(percent_reduce)
    final_cd = after_cdr_percent * (1 - percent_reduce)
    #print(final_cd)
    return round(final_cd,4)

def bite_cd_calc(hexa_bite_level, cdr_percent, cdr_potential):
    if hexa_bite_level < 0 or hexa_bite_level > 30:
        print("Invalid level")
        return 0
    hexa_bite_cd = 15 - math.ceil(hexa_bite_level/6)
    return calculate_final_cd(hexa_bite_cd, cdr_percent, cdr_potential)

print(bite_cd_calc(25,5,4))
