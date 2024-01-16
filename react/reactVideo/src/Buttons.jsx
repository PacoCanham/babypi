import Button from '@mui/material/Button';

export default function Buttons({btnid, handleClick, variant = "contained", content=" "}) {
    return (<Button id={btnid} onClick={handleClick} variant={variant}>{content}</Button>);
}
