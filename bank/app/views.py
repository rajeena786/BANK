from django.shortcuts import render,HttpResponse
from .forms import AccountForm
from django.core.mail import send_mail
from django.conf import settings
from .models import Account
# Create your views here.
def home(request):
    return render(request,"index.html")

def create(request):
    form=AccountForm()
    if request.method =="POST":
        form=AccountForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            print("successful")
            # print(form.data)
            reciver_email = form.data["email"]
            data = Account.objects.get(email =reciver_email)
            acc = data.account_number

            try:
                send_mail(
                    "Thanks for Registration", #subject
                    f"Thanks you for Registering with our probank. weare excited to have you on board! your account number is <h1>{acc}</h1> ,\n thank you \n regards probank manager ",#body
                    settings.EMAIL_HOST_USER,
                    [reciver_email],
                    fail_silently=False
                )
                print("mail sent")
            except Exception as e:
                return HttpResponse(f"Error sending email:{e}")



    return render(request,"create.html",{'form':form})    

def pin(request):
    form=AccountForm()
    if request.method =="POST":
        acc=request.POST.get('account_number')
        moblie=request.POST.get('moblie')
        pin=int(request.POST.get('pin'))
        cpin=int(request.POST.get('pin'))
        print(acc,moblie,pin,cpin)
        try:
            account = Account.objects.get(account_number = acc)
        except:
            return HttpResponse("account not found in database")
        finally:
            print("exception is handled")  
        if account.mobile == int(moblie):
            if pin == cpin:
                pin +=111
                account.pin = pin
                account.save()
            # Sending email confirmation
                try:
                    send_mail(
                        "PIN Generated Successfully",
                        f"Dear {account.name},\n\nYour PIN has been successfully created for your account {acc}. Please keep it secure.\n\nThank you,\nProBank Team",
                        settings.EMAIL_HOST_USER,
                        [account.email],
                        fail_silently=False,
                    )
                    print("PIN generation email sent")
                except Exception as e:
                    return HttpResponse(f"Error while pin generator sending Email: {e}")
                return HttpResponse("PIN generated successfully, and email sent.")
            else:
                return HttpResponse("Both PINs do not match.")
        else:
            return HttpResponse("Mobile number does not match our records.")
    
    return render(request, "pin.html", {'form': form})
        
         

    return render(request,"pin.html")    

def balance(request):
    bal = 0
    var=False
    if request.method == "POST":
        var=True
        acc = request.POST.get("acc")
        pin = int(request.POST.get("pin"))
        print(acc,pin)
        try:
            account = Account.objects.get(account_number = acc)
            print(account)
        except:
             return HttpResponse("account not found")
        encpin = account.pin-111
        if pin == encpin:
            print("pin matched")
            bal = account.balance
        else:
            return HttpResponse("pin did'nt match")
    return render(request,"balance.html",{"bal":bal,"var":var})    
   

def depist(request):
    bal=0
    if request.method == "POST":
        acc = request.POST.get("acc")
        phone = int(request.POST.get("mobile"))
        amt =int(request.POST.get("amount"))
        # print(acc,phone,amt)
        try:
            accoount = Account.objects.get(account_number = acc)
            # print(account)
        except:
            return HttpResponse("acc nt found")
        finally:
            print("exception is hanadle")
            # print(accoount.mobile)     
        if accoount.mobile == phone:
            print("acc is verified")
            if amt >=100 and amt <= 100000:
                accoount.balance += amt
                accoount.save()
                reciver_email = accoount.email
                try:
                    send_mail(
                        "Deposit successful", #subject
                        f"dear {accoount.name},\n\nYou have successfully deposited {amt} into your account {acc}.\nYour updated balance is {bal}.\n\nThank yu,\nProBank team" ,#body
                        settings.EMAIL_HOST_USER,
                        [reciver_email],
                        fail_silently=False
                    )
                    print("mail sent")
                except Exception as e:
                    return HttpResponse(f"Error sending email:")
            else:
                return HttpResponse("please enter the proper amt to deposit")
        else:
            return HttpResponse("enter the valid mbile number")       
    return render(request,"depist.html",{'bal':bal})

def withdraw(request):
    bal = 0
    if request.method == "POST":
        acc = request.POST["acc"]
        pin = int(request.POST["pin"])
        amt = int(request.POST["amt"])
        # print(acc,pin,amt)
        try:
            accoount =Account.objects.get(account_number = acc)
            # print(account)
        except:
            return HttpResponse("acc not found")
        finally:
            print("exception is hanadle")
        check_pin = accoount.pin-111
        if check_pin == pin:  
            print("pin matched")
            if accoount.balance > amt and amt<=10000 and amt >=500:
                accoount.balance -= amt  
                accoount.save()
                bal = accoount.balance
                reciver_email = accoount.email

                try:
                 send_mail(
                    "withdrawal Successful", #subject
                    f"dear {accoount.name},\n\nYou have successfully withdrawn {amt} from your account {acc}.\nYour udated balance is{bal}.\n\nThank your,\nProBank Team",#body
                    settings.EMAIL_HOST_USER,
                    [reciver_email],
                    fail_silently=False
                )
                 print("mail sent")
                except Exception as e:
                    return HttpResponse(f"Error sending email:{e}")
            else:
                return HttpResponse("please enter the valid amount")
    else:
        print("enter the valid pin")            
    return render(request,"withdraw.html",{"bal":bal})     

def acctrancefore(request):
    if request.method == "POST":
        acc = request.POST["acc"]
        tacc = request.POST["tacc"]
        amt = int(request.POST.get("amt"))
        pin = int(request.POST.get("pin"))
        print(acc,amt,tacc,pin)
        try:
            accoount =Account.objects.get(accoount_number = acc)
            # print(account)
        except:
            return HttpResponse("acc not found")
        finally:
            print("exception is hanadle for frm acc")
        try:
            to_accoount =Accoount.objects.get(accoount_number = tacc)
            # print(account)
        except:
            return HttpResponse("tacc not found")
        finally:
            print("exception is hanadle for frm tacc")
        check_pin = accoount.pin-111
        if check_pin ==pin:
            if accoount.balance > amt :
                accoount.balance-=amt
                to_accoount.balance+=amt
                accoount.save()
                to_accoount.save()
         
                # return HttpResponse(f"Transfer successful. Updated balance: {account.balance}")
            else:
                return HttpResponse("Insufficient balance.")
        else:
            return HttpResponse("Incorrect PIN.")
    return render(request, "acctrancefore.html")
           