rating_table = [
    [],
    [0.05,0.1,0.2,0.3,0.4,0.5,0.7],
    [],
    []
]

def rating(students,r):
    s = [0]*7
    for student in students:
        s[0] += (student == 300)
        s[1] += (290 <= student < 300)
        s[2] += (280 <= student < 290)
        s[3] += (270 <= student < 280)
        s[4] += (260 <= student < 270)
        s[5] += (250 <= student < 260)
        s[6] += (student < 250)
    return round(sum(i * rating_table[r][n] for n,i in enumerate(s)))

    

def main():
    print(rating([226, 261, 297, 232, 266, 238, 299, 215, 235, 238, 202, 265, 273, 252,
            245, 292, 233, 281, 255, 226, 255, 238, 299, 242, 270, 282, 240, 230, 287, 295],1))
if __name__ == "__main__": 
    main()