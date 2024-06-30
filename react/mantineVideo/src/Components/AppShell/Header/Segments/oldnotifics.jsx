import { useDisclosure } from '@mantine/hooks';
import { Modal, Button, Box, Slider, Stack } from '@mantine/core';

const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: '90%',
    height: '90%',
    bgcolor: 'background.paper',
    border: '2px solid red',
    borderRadius : '5%',
    boxShadow: 24,
    p: 4,
    textAlign: 'center',
    overflowY: 'auto', // Add scroll bar if content is too long
    '@media (min-width:600px)': {
      width: '80%',
      height: '70%',
    },
    '@media (min-width:960px)': {
      width: '60%',
      height: '60%',
    },
    '@media (min-width:1280px)': {
      width: '50%',
      height: '50%',
    },
    '@media (min-width:1920px)': {
      width: '40%',
      height: '40%',
    },
  };
  

export default function VideoNotificationModal(props) {
    const notificationDict = {
        movNumHigh: 100,
        movNumLow: 0,
        movThres: 60,
        notificationDelay: 600,
        delayHigh:60,
        delayLow:5,
        rmsLow:500,
        rmsHigh:1400,
        timeSample:3,
        
    };
    
    return (
    <>
      <Modal opened={props.modal} onClose={props.close} title="Authentication">
        
      <Box sx={style}>
        <hr/>
        <Text id="modal-modal-title" variant="h6" component="h2" sx={{color:"black"}}>
          Video Notification Settings
        </Text>
        <hr/>
        <Box sx={{ width: 'auto', align:'center'}}>
        <Text sx={{color:"black"}} gutterBottom>Movement Threshold</Text>
        <Slider min={5} max={100} step={5}valueLabelDisplay="auto" name='movThres' value={notificationDict.movThres}  />
        <Text sx={{color:"black"}} gutterBottom>Number of seconds of movement before Low Notification</Text>
        <Slider min={1} max={notificationDict.movNumHigh} valueLabelDisplay="auto" name='movNumLow' value={notificationDict.movNumLow}  />
        <Text sx={{color:"black"}} gutterBottom>Number of seconds of movement before High Notification</Text>
        <Slider min={notificationDict.movNumLow} max={60} valueLabelDisplay="auto" name='movNumHigh' value={notificationDict.movNumHigh}  />
        <Text sx={{color:"black"}} gutterBottom>Number of seconds seconds between Low Notifications</Text>
        <Slider min={1} max={1200} step={10} valueLabelDisplay="auto" name='notificationDelay' value={notificationDict.notificationDelay}  />
        </Box>
        <hr/>
        <Text id="modal-modal-subtitle" variant="h6" component="h2" sx={{color:"black"}}>
          Audio Notification Settings
        </Text>
        <hr/>
        <Box sx={{ width: 'auto', align:'center'}}>
        <Text sx={{color:"black"}} gutterBottom>Delay between REALLY Loud noises</Text>
        <Slider min={5} max={60} step={5}valueLabelDisplay="auto" name='delayHigh' value={notificationDict.delayHigh}  />
        <Text sx={{color:"black"}} gutterBottom>Delay between less Loud noises</Text>
        <Slider min={5} max={60} step={5} valueLabelDisplay="auto" name='delayLow' value={notificationDict.delayLow}  />
        <Text sx={{color:"black"}} gutterBottom>Volume (RMS) to trigger the LOW notification</Text>
        <Slider min={500} max={notificationDict.rmsHigh} valueLabelDisplay="auto" name='rmsLow' value={notificationDict.rmsLow}  />
        <Text sx={{color:"black"}} gutterBottom>Volume (RMS) to trigger the HIGH notification</Text>
        <Slider min={notificationDict.rmsLow} max={3000} step={50} valueLabelDisplay="auto" name='rmsHigh' value={notificationDict.rmsHigh}  />
        <Text sx={{color:"black"}} gutterBottom>Numbver of seconds to listen to make the average</Text>
        <Slider min={1} max={10} valueLabelDisplay="auto" name='timeSample' value={notificationDict.timeSample}  />

        </Box>
        <Stack direction="row"   justifyContent="center" alignItems="center" spacing={2}>
        <Button variant="contained" color="success" >Apply</Button>
        <Button variant="contained" color="secondary" >Cancel</Button>
        <Button variant="contained" color="error" >Reset</Button>
        </Stack>
      </Box>
      </Modal>

      <Button onClick={open}>Open modal</Button>
    </>
  );
}