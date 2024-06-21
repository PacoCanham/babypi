import { Button, Group, SimpleGrid } from "@mantine/core";
import { IconArrowDown, IconArrowLeft, IconArrowRight, IconArrowUp } from "@tabler/icons-react";

export default function Controls(){
    function handleClick(e) {
        e.preventDefault();
        let url =  (e.currentTarget.id);
        async function moveCamera(e) {
            // sends a get request to /settings
            const response = await fetch(url);
        }
        moveCamera();
    }

    return (
    <SimpleGrid
    cols={1}
    spacing='xs'
    verticalSpacing='xs'>
        <Group justify="center" gap='xs'>
    <Button id="/up" w={221} handleClick={handleClick}>{<IconArrowUp/>}</Button>	
    </Group>	
            <Group justify="center" gap='xs'>
                <Button w={200/3} id="/left" handleClick={handleClick}>{<IconArrowLeft/>}</Button>				
                <Button w={200/3} id="/flip" handleClick={handleClick}>FLIP</Button>				
                <Button w={200/3} id="/right" handleClick={handleClick}>{<IconArrowRight/>}</Button>			
            </Group>
            <Group justify="center" gap='xs'>
    <Button id="/down" w={221} handleClick={handleClick}>{<IconArrowDown/>}</Button>		
    </Group>		
    </SimpleGrid>
    )
}