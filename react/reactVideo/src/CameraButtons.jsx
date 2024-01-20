import * as React from 'react';
import ButtonGroup from '@mui/material/ButtonGroup';
import { KeyboardArrowLeftSharp, KeyboardArrowRightSharp, KeyboardArrowUpSharp, KeyboardArrowDownSharp} from '@mui/icons-material';
import Buttons from './Buttons';

export default function CameraButtons() {
    function handleClick(e) {
        e.preventDefault();
        let url =  (e.currentTarget.id);
        async function moveCamera(e) {
            // sends a get request to /settings
            const response = await fetch(url);
        }
        moveCamera();
       if (e.currentTarget.id == 'flip'){
            setTimeout(()=>{location.reload()}, 3000);
        }
    }

 return (
	<div>
		<ButtonGroup  size="Large"  orientation="vertical" variant="contained">
        <Buttons sx={{borderTopRightRadius:"100%", borderTopLeftRadius:"100%"}} btnid="up" handleClick={handleClick} content={<KeyboardArrowUpSharp/>}/>				
                <ButtonGroup size="Large" variant="contained">
                    <Buttons btnid="left" handleClick={handleClick} content={<KeyboardArrowLeftSharp/>}/>				
                    <Buttons btnid="flip" handleClick={handleClick} content='FLIP'/>				
                    <Buttons btnid="right" handleClick={handleClick} content={<KeyboardArrowRightSharp/>}/>			
                </ButtonGroup>
                <Buttons btnid="down" sx={{borderBottomRightRadius:"100%", borderBottomLeftRadius:"100%"}} handleClick={handleClick} content={<KeyboardArrowDownSharp/>}/>				
		</ButtonGroup>
	</div>
  );
}
