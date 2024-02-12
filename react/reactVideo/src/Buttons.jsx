import Button from '@mui/material/Button';

export default function Buttons({btnid, handleClick, variant = "contained", content=" ", sx = ''}) {
    return (<Button sx={{sx}} key={btnid} id={btnid} onClick={handleClick} variant={variant}>{content}</Button>);
}
