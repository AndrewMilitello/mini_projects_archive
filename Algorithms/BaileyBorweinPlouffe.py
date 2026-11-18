#implementation of BBP algorithm to calculate the nth digit of pi for Pi day 2024
import numpy as np
import decimal
#uses bailey borwein plouffe π = Σk=0 to ∞ 16-k [ 4/(8k+1) – 2/(8k+4) – 1/(8k+5) – 1/(8k+6) ]
#n_hex_digits to compute is 1.3* the input amt of digits to ensure accuracy
#do the summation formula, return a list of hex digits of pi
#get the hex expansion and convert to base 10
#drop the integer and multiply the fractional part by 10^(n-1)
#drop the integer again and the tenth's place decimal is the one remaining.


def d(n):
    return decimal.Decimal(n)
def decimal_borwein_ploufe(k):
    return(d(1)/(d(16)**k)*(d(4)/d(8*k+1) - d(2)/d(8*k+4) - d(1)/d(8*k+5) - d(1)/d(8*k+6)))
def bailey_borwein_plouffe(n):
    n = int(n)
    n_hex_digits = np.ceil(n*1.3)
    decimal.getcontext().prec = n+10
    sum = 0
    for k in range(int(n_hex_digits)):
        sum += decimal_borwein_ploufe(k)
    return(str(int((sum%1)*10**(n)))[n-1])
    
print(bailey_borwein_plouffe(input("Choose a digit of pi to calculate:")))
    
