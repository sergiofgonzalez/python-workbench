

def find(nums, n):
    def print_status():
        print("start:", start)
        print("mid  :", mid)
        print("end  :", end)

    start = 0
    end = len(nums) - 1
    mid = (end - start) // 2

    while nums[mid] 


nums = [0, 1, 2, 3]
find(nums, 1)
