import {
    Box,
    Button,
    Divider,
    Flex,
    SegmentedControl,
    Slider,
    Stack,
    Switch,
    Text,
} from "@mantine/core";
import { useSetState } from "@mantine/hooks";
import { useEffect, useState } from "react";

const defaultNotificationDict = {
    Vee: {
        delayLow: 600,
        delayHigh: 1800,
        volumeLow: 100,
        volumeHigh: 1000,
        sampleLength: 3,
        enabled: true,
    },
    Paco: {
        delayLow: 600,
        delayHigh: 1800,
        volumeLow: 100,
        volumeHigh: 1000,
        sampleLength: 3,
        enabled: true,
    },
};

export default function AudioNotificationModal(props) {
    const [notificationDict, setNotificationDict] = useSetState(
        defaultNotificationDict
    );

    const [user, setUser] = useState("Paco");

    async function initObjects() {
        await fetch("/getAudioConfig")
            .then((response) => response.json())
            .then((data) => {setNotificationDict(data.settings);setUser(data.username)});
    }

    useEffect(() => {
        initObjects();
    }, []);

    async function applyAudio() {
        await fetch("/applyAudio", {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(notificationDict),
        });
    }

    function cancelAudio() {
        initObjects();
    }

    async function resetAudio() {
        setNotificationDict(defaultNotificationDict);
        await fetch("/applyAudio", {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(defaultNotificationDict),
        });
    }

    return (
        <Box h={"50vh"}>
            <Stack
                h={300}
                bg="var(--mantine-color-body)"
                align="stretch"
                justify="flex-start"
                gap="xs"
            >
                <Stack
                h={300}
                bg="var(--mantine-color-body)"
                align="center"
                justify="flex-start"
                gap="xs"
            >
                <Switch size="xl" onLabel="ON" offLabel="OFF" checked={notificationDict[user].enabled} onClick={()=>setNotificationDict({
                                    [user]: {
                                        delayLow: notificationDict[user].delayHigh,
                                        delayHigh:
                                            notificationDict[user].delayHigh,
                                        volumeLow:
                                            notificationDict[user].volumeLow,
                                        volumeHigh:
                                            notificationDict[user].volumeHigh,
                                        sampleLength:
                                            notificationDict[user].sampleLength,
                                        enabled: !notificationDict[user].enabled,
                                    }})} />
                </Stack>
                <Stack
                    h={300}
                    bg="var(--mantine-color-body)"
                    align="stretch"
                    justify="flex-start"
                    gap="xs"
                >
                    <SegmentedControl
                        defaultValue={user}
                        size="md"
                        radius="lg"
                        data={["Paco", "Vee"]}
                        onChange={setUser}
                    />
                </Stack>
                <Stack
                    h={300}
                    bg="var(--mantine-color-body)"
                    align="stretch"
                    justify="flex-start"
                    gap="xs"
                >
                    <Stack
                        h={300}
                        bg="var(--mantine-color-body)"
                        align="stretch"
                        justify="flex-start"
                        gap="xs"
                    >
                        <Text>Quiet noise Delay</Text>
                        <Slider
                            value={notificationDict[user].delayLow}
                            color="blue"
                            radius="md"
                            min={1}
                            max={notificationDict[user].delayHigh}
                            onChangeEnd={(v) =>
                                setNotificationDict({
                                    [user]: {
                                        delayLow: v,
                                        delayHigh:
                                            notificationDict[user].delayHigh,
                                        volumeLow:
                                            notificationDict[user].volumeLow,
                                        volumeHigh:
                                            notificationDict[user].volumeHigh,
                                        sampleLength:
                                            notificationDict[user].sampleLength,
                                        enabled: notificationDict[user].enabled,
                                    },
                                })
                            }
                            step={10}
                            label={(v) => `${v / 60}m`}
                            marks={[
                                { value: 1, label: "1s" },
                                { value: 60, label: "1m" },
                                { value: 600, label: "10m" },
                                { value: 1800, label: "30m" },
                                { value: 3600, label: "1hr" },
                            ]}
                        />
                    </Stack>
                    <Stack
                        h={300}
                        bg="var(--mantine-color-body)"
                        align="stretch"
                        justify="flex-start"
                        gap="xs"
                    >
                        <Text>Loud Noise Delay</Text>
                        <Slider
                            value={notificationDict[user].delayHigh}
                            color="blue"
                            radius="md"
                            min={notificationDict[user].delayLow}
                            max={3600}
                            onChangeEnd={(v) =>
                                setNotificationDict({
                                    [user]: {
                                        delayLow:
                                            notificationDict[user].delayLow,
                                        delayHigh: v,
                                        volumeLow:
                                            notificationDict[user].volumeLow,
                                        volumeHigh:
                                            notificationDict[user].volumeHigh,
                                        sampleLength:
                                            notificationDict[user].sampleLength,
                                        enabled: notificationDict[user].enabled,
                                    },
                                })
                            }
                            step={10}
                            label={(v) => `${v / 1000}s`}
                            marks={[
                                { value: 20, label: "20%" },
                                { value: 50, label: "50%" },
                                { value: 80, label: "80%" },
                            ]}
                        />
                    </Stack>
                    <Stack
                        h={300}
                        bg="var(--mantine-color-body)"
                        align="stretch"
                        justify="flex-start"
                        gap="xs"
                    >
                        <Text>Low Notification Volume</Text>
                        <Slider
                            value={notificationDict[user].volumeLow}
                            color="blue"
                            radius="md"
                            min={10}
                            max={notificationDict[user].volumeHigh}
                            onChangeEnd={(v) =>
                                setNotificationDict({
                                    [user]: {
                                        delayLow:
                                            notificationDict[user].delayLow,
                                        delayHigh:
                                            notificationDict[user].delayHigh,
                                        volumeLow: v,
                                        volumeHigh:
                                            notificationDict[user].volumeHigh,
                                        sampleLength:
                                            notificationDict[user].sampleLength,
                                        enabled: notificationDict[user].enabled,
                                    },
                                })
                            }
                            step={10}
                        />
                    </Stack>
                    <Stack
                        h={300}
                        bg="var(--mantine-color-body)"
                        align="stretch"
                        justify="flex-start"
                        gap="xs"
                    >
                        <Text>High Notification Volume</Text>
                        <Slider
                            value={notificationDict[user].volumeHigh}
                            color="blue"
                            radius="md"
                            min={notificationDict[user].volumeLow}
                            max={3000}
                            onChangeEnd={(v) =>
                                setNotificationDict({
                                    [user]: {
                                        delayLow:
                                            notificationDict[user].delayLow,
                                        delayHigh:
                                            notificationDict[user].delayHigh,
                                        volumeLow:
                                            notificationDict[user].volumeLow,
                                        volumeHigh: v,
                                        sampleLength:
                                            notificationDict[user].sampleLength,
                                        enabled: notificationDict[user].enabled,
                                    },
                                })
                            }
                            step={10}
                        />
                    </Stack>
                    <Stack
                        h={300}
                        bg="var(--mantine-color-body)"
                        align="stretch"
                        justify="flex-start"
                        gap="xs"
                    >
                        <Text>Lengh of Sample</Text>
                        <Slider
                            value={notificationDict[user].sampleLength}
                            color="blue"
                            radius="md"
                            min={1}
                            max={10}
                            onChangeEnd={(v) =>
                                setNotificationDict({
                                    [user]: {
                                        delayLow:
                                            notificationDict[user].delayLow,
                                        delayHigh:
                                            notificationDict[user].delayHigh,
                                        volumeLow:
                                            notificationDict[user].volumeLow,
                                        volumeHigh:
                                            notificationDict[user].volumeHigh,
                                        sampleLength: v,
                                        enabled: notificationDict[user].enabled,
                                    },
                                })
                            }
                            step={1}
                            label={(v) => `${v}s`}
                            marks={[
                                { value: 1, label: "1s" },
                                { value: 5, label: "5s" },
                                { value: 10, label: "10s" },
                            ]}
                        />
                    </Stack>
                </Stack>
                <Divider />
                <Stack
                    h={300}
                    bg="var(--mantine-color-body)"
                    align="stretch"
                    justify="flex-start"
                    gap="xs"
                >
                    <Flex
                        mih={50}
                        gap="md"
                        justify="center"
                        align="flex-end"
                        direction="row"
                        wrap="wrap"
                    >
                        <Button
                            variant="filled"
                            size="md"
                            radius="lg"
                            onClick={applyAudio}
                        >
                            Apply
                        </Button>
                        <Button
                            variant="filled"
                            color="green"
                            size="md"
                            radius="lg"
                            onClick={cancelAudio}
                        >
                            Cancel
                        </Button>
                        <Button
                            variant="filled"
                            color="red"
                            size="md"
                            radius="lg"
                            onClick={resetAudio}
                        >
                            Reset
                        </Button>
                    </Flex>
                </Stack>
            </Stack>
        </Box>
    );
}
