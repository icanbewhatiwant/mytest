import re



if __name__=="__main__":

    test_str = "③硬脊膜外阻滞时，0.25%〜0.375%溶液，"
    test_end = "10〜20ml用于中上腹部手术。"
    rongye_end_patr = re.compile("(\d*\.?\d*%?[-|〜|~]?\d*\.?\d*%?溶液[,，])$")
    ml_begin_patr = re.compile("^(\d*\.?\d*[-|〜|~]?\d*\.?\d*(mg\/kg|mg|ml|g))")
    ret = rongye_end_patr.search(test_str)
    end = ml_begin_patr.search(test_end)

    print(ret.group())
    print(end.group())