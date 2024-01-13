import * as React from 'react';
import Button from '@mui/material/Button';
import ButtonGroup from '@mui/material/ButtonGroup';
import { KeyboardArrowLeftSharp, KeyboardArrowRightSharp, KeyboardArrowUpSharp, KeyboardArrowDownSharp} from '@mui/icons-material';

export default function Buttons() {
    function handleClick(e) {
        e.preventDefault();
        let url = "http://192.168.4.50:5000/" + (e.currentTarget.id);
        async function moveCamera() {
            // sends a get request to /settings
            const response = await fetch(url);
            // console.log(url)
        }
        moveCamera();
	if (e.currentTarget.id == 'flip') {
		window.location.reload();		
	}
    }


  return (
	<div>
		<ButtonGroup size="Large"  orientation="vertical" variant="contained" aria-label="outlined primary button group">
            <Button id='up' name='up' onClick={handleClick} variant='contained'><KeyboardArrowUpSharp/></Button>
                <ButtonGroup size="Large" variant="contained" aria-label="outlined primary button group">
                    <Button id='left' onClick={handleClick} variant='contained'><KeyboardArrowLeftSharp/></Button>				
                    <Button id='flip' onClick={handleClick}>Flip</Button>
                    <Button id='right' onClick={handleClick} variant='contained'><KeyboardArrowRightSharp/></Button>
                </ButtonGroup>
            <Button id='down' onClick={handleClick} variant='contained'><KeyboardArrowDownSharp/></Button>
		</ButtonGroup>
	</div>
  );
}
