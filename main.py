import struc_manip as sm

if __name__ == '__main__':
    location = "D:\\Pictures"
    print(sm.get_duplicates(location, exclude="D:\\Pictures\\Unsortables"))