# Raspi project

## download file

install dependencies by
```bash
python3 install -t requirements.txt
```

## Push to raspi nano
### Connect via ssh
### generate key
#### with: 
```bash
ssh keygen
```
#### Then load the pub key to your raspberry
### connect to raspi and pull code via 
```bash
git clone https://github.com/devrema/raspi.git
```

### Let code run on start with:

```bash
sudo corntab -e
```

then add 
```
@reboot <Path_To_Your_Project.py> &
```
 at the end of the crontab file. DONT'T FORGET THE "&"