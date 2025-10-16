# Guest Additions Setup Guide for VirtualBox VM

## Current Issue
Your VM behavioral analysis is failing because Guest Additions are not properly configured in your Windows 10 VM.

## Solution Options

### Option 1: Install Guest Additions (Recommended)
1. Start your SandboxWin10 VM in GUI mode (not headless)
2. In the VM window, go to: **Devices → Insert Guest Additions CD image**
3. In Windows 10 VM, open File Explorer and run the Guest Additions installer
4. Reboot the VM
5. Create a new clean snapshot after Guest Additions are installed

### Option 2: Use Shared Folders (Alternative)
1. Power off your VM
2. In VirtualBox Manager:
   - Right-click SandboxWin10 → Settings
   - Go to Shared Folders
   - Add a new shared folder:
     - Folder Path: `C:\Users\sayha\Final Year Project\shared`
     - Folder Name: `samples`
     - Check "Auto-mount" and "Make Permanent"
3. Start VM and access samples via shared folder

### Option 3: Manual File Placement (Quick Test)
1. Create a shared folder or use VM's existing drives
2. Manually copy sample files to VM
3. Use network monitoring tools in the VM
4. Monitor changes via VM screenshots and logs

## Commands to Test Guest Additions
Run these in your Windows 10 VM to check Guest Additions status:

```cmd
# Check if VBoxService is running
tasklist | findstr VBox

# Check Guest Additions version
"C:\Program Files\Oracle\VirtualBox Guest Additions\VBoxControl.exe" --version

# Test file sharing
net use
```

## VM Configuration Requirements
- **RAM**: At least 2GB for Windows 10
- **CPU**: 2+ cores recommended
- **Network**: NAT or Host-Only for isolation
- **Username**: sandbox
- **Password**: 0409 (already configured)

## Next Steps After Guest Additions Setup
1. Test file copy: `VBoxManage guestcontrol SandboxWin10 copyto --help`
2. Test command execution: `VBoxManage guestcontrol SandboxWin10 run --help`
3. Re-run the behavioral analysis script

## Alternative: Manual VM Monitoring
If Guest Additions can't be installed, we can:
1. Use VM snapshots and screenshots
2. Monitor process lists via Task Manager
3. Use built-in Windows monitoring tools
4. Extract logs manually after execution
