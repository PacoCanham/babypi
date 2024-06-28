import { Button, Group, SimpleGrid } from "@mantine/core";
import { IconArrowDown, IconArrowLeft, IconArrowRight, IconArrowUp } from "@tabler/icons-react";

export default function Controls(){

    return (
    <SimpleGrid
    cols={1}
    spacing='xs'
    verticalSpacing='xs'>
        <Group justify="center" gap='xs'>
    <Button w={221} onClick={()=>fetch("/move/up")}>{<IconArrowUp/>}</Button>	
    </Group>	
            <Group justify="center" gap='xs'>
                <Button w={200/3} onClick={()=>fetch("/move/left")}>{<IconArrowLeft/>}</Button>				
                <Button w={203/3} onClick={()=>fetch("/flip")}>FLIP</Button>				
                <Button w={200/3} onClick={()=>fetch("/move/right")}>{<IconArrowRight/>}</Button>			
            </Group>
            <Group justify="center" gap='xs'>
    <Button w={221} onClick={()=>fetch("/move/down")}>{<IconArrowDown/>}</Button>		
    </Group>		
    </SimpleGrid>
    )
}