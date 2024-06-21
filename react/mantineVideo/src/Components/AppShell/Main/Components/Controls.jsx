import { Button, Group, SimpleGrid } from "@mantine/core";
import { IconArrowDown, IconArrowLeft, IconArrowRight, IconArrowUp } from "@tabler/icons-react";

export default function Controls(){

    return (
    <SimpleGrid
    cols={1}
    spacing='xs'
    verticalSpacing='xs'>
        <Group justify="center" gap='xs'>
    <Button id="/up" w={221} onClick={()=>fetch("/up")}>{<IconArrowUp/>}</Button>	
    </Group>	
            <Group justify="center" gap='xs'>
                <Button w={200/3} id="/left" onClick={()=>fetch("/left")}>{<IconArrowLeft/>}</Button>				
                <Button w={203/3} id="/flip" onClick={()=>fetch("/flip")}>FLIP</Button>				
                <Button w={200/3} id="/right" onClick={()=>fetch("/right")}>{<IconArrowRight/>}</Button>			
            </Group>
            <Group justify="center" gap='xs'>
    <Button id="/down" w={221} onClick={()=>fetch("/down")}>{<IconArrowDown/>}</Button>		
    </Group>		
    </SimpleGrid>
    )
}