from rpy2.robjects import r

r('''
   isPrimeFunc <- function(n){
   x<-c()
   vectorN <- 1:n
   for (i in vectorN){
      if (i == 2) {
         flag <- TRUE
      } else if (any(i %% 2:(i-1) == 0)) {
         flag <- FALSE
      } else { 
         flag <- TRUE
      }
      
      if (flag){
         x<-append(x,vectorN[i])
      }
   }
   return(x)
   }
   ''')

def isPrimeFunc(n):
   primeNumList = []
   allNumbers = range(1, n+1)

   for i in range(2,n+1): # no need to consider the num 1
      if i==2:
         flag=True
      elif any([(i % j)==0 for j in range(2,i)]):
         flag=False
      else:
         flag=True
      
      if flag: primeNumList.append(allNumbers[i-1])

   return primeNumList
