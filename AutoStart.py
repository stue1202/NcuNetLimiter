from tkinter import filedialog, messagebox
import winreg
import os
 
# 获取当前用户的启动项注册表路径
startup_reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
startup_reg_key = winreg.HKEY_CURRENT_USER

def add_startup_item(file_path):
    try:
        filename = os.path.basename(file_path)
        key = winreg.OpenKey(startup_reg_key, startup_reg_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, filename, 0, winreg.REG_SZ, file_path)
        winreg.CloseKey(key)
        messagebox.showinfo("添加启动项", f"已成功添加启动项: {filename}")
    except Exception as e:
        messagebox.showerror("添加启动项失败", f"添加启动项时出错: {str(e)}")
 
def remove_startup_item(item_name):
    try:
        key = winreg.OpenKey(startup_reg_key, startup_reg_path, 0, winreg.KEY_WRITE)
        winreg.DeleteValue(key, item_name)
        winreg.CloseKey(key)
        messagebox.showinfo("删除启动项", f"已成功删除启动项: {item_name}")
    except FileNotFoundError:
        messagebox.showwarning("删除启动项", f"启动项 '{item_name}' 不存在")
    except Exception as e:
        messagebox.showerror("删除启动项失败", f"删除启动项时出错: {str(e)}")