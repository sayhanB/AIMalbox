# VM Configuration for Malware Analysis

## SandboxWin10 VM Setup

### Current Status: ✅ VM Controller Working
- VM Name: SandboxWin10
- State: Detected and controllable
- Snapshots: CleanState, clean (newly created)
- VirtualBox Integration: Working

### Required Information
Please provide the following for your Windows 10 VM:

1. **Username**: [Your Windows 10 VM username]
2. **Password**: [Your Windows 10 VM password]
3. **Guest Additions**: Are Guest Additions installed? (Required for file transfer)

### Network Configuration
- VM Network Mode: NAT/Bridged/Host-Only?
- VM IP Address: [If known]

### Next Steps
1. ✅ VM Controller tested and working
2. 🔄 Configure VM credentials
3. 🔄 Test Guest Additions and file transfer
4. 🔄 Set up monitoring agents in VM
5. 🔄 Create malware analysis pipeline

### Commands to Run in VM (if Guest Additions working)
```bash
# Create analysis directory
mkdir C:\analysis
mkdir C:\analysis\samples
mkdir C:\analysis\logs

# Install monitoring tools (if needed)
# We'll add process monitor, file monitor, etc.
```

### Security Notes
- VM should be isolated (no internet access during analysis)
- Clean snapshots before each analysis
- Monitor for VM escapes
- Regular snapshot management
