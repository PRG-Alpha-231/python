# class Institution:
#     name="skillmentor"
#     place="mankavu"
#     no="9526493748"
#     def __init__(self,pincode,no_of_students):
#         self.pincode=pincode
#         self.no_of_students=no_of_students
        
#     def print_data(self):
#         print("constructor working",self.pincode,self.no_of_students)


# object1=Institution(673007,23)
# object2=Institution(586003,45)
# object1.print_data()
# object2.print_data()
class A:
    def print_class_a(self):
        print("this is class A")
    

class B(A):
    @staticmethodls
    
    def print_class_b():
        print("this is class B")
    def find_sum(self,no_1,no_2):
        
        sum=no_1+no_2
        print(sum)

object1=B()
object1.print_class_b()  
object1.find_sum(no_1=10,no_2=34)        
