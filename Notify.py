# modules
from win10toast_click import ToastNotifier 
import Info
# function 
ForImport=1
def notify(title,content):
    # initialize 
    toaster = ToastNotifier()
    # showcase
    toaster.show_toast(
        title, # title
        content, # message 
         # 'icon_path' 
        duration=0.5, # for how many seconds toast should be visible; None = leave notification in Notification Center
        threaded=True # True = run other code in parallel; False = code execution will wait till notification disappears  # click notification to run function 
        )