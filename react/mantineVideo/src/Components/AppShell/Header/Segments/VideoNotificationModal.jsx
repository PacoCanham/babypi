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
        movThres: 60,
        movNumLow: 3,
        movNumHigh: 30,
        notificationDelay: 600,
        enabled: true,
    },
    Paco: {
        movThres: 250,
        movNumLow: 3,
        movNumHigh: 30,
        notificationDelay: 600,
        enabled: true,
    },
};
export default function VideoNotificationModal(props) {
    const [notificationDict, setNotificationDict] = useSetState(
        defaultNotificationDict
    );
    const [user, setUser] = useState("Paco");

    async function initObjects() {
        await fetch("/getVideoConfig")
            .then((response) => response.json())
            .then((data) => setNotificationDict(data));
    }

    async function applyVideo() {
        await fetch("/applyVideo", {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(notificationDict),
        });
    }

    function cancelVideo() {
        initObjects();
    }

    async function resetVideo() {
        setNotificationDict(defaultNotificationDict);
        await fetch("/applyVideo", {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(defaultNotificationDict),
        });
    }

    useEffect(() => {
        initObjects();
    }, []);

    return (
        <Box h={"50vh"}>
            <Stack
                h={300}
                bg="var(--mantine-color-body)"
                align="stretch"
                justify="flex-start"
                gap="xs"
            >                <Stack
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
                        <Text>Movement Threshold</Text>
                        <Slider
                            min={0}
                            max={255}
                            step={5}
                            name="movThres"
                            value={notificationDict[user].movThres}
                            color="blue"
                            radius="md"
                            label={(v) => `${((v / 255) * 100).toFixed(0)}%`}
                            marks={[
                                { value: 0, label: "0%" },
                                { value: 127.5, label: "50%" },
                                { value: 255, label: "100%" },
                            ]}
                            onChangeEnd={(v) =>
                                setNotificationDict({
                                    [user]: {
                                        movThres: v,
                                        movNumLow:
                                            notificationDict[user].movNumLow,
                                        movNumHigh:
                                            notificationDict[user].movNumHigh,
                                        notificationDelay:
                                            notificationDict[user]
                                                .notificationDelay,
                                        enabled: notificationDict[user].enabled,
                                    },
                                })
                            }
                        />
                    </Stack>
                    <Stack
                        h={300}
                        bg="var(--mantine-color-body)"
                        align="stretch"
                        justify="flex-start"
                        gap="xs"
                    >
                        <Text>
                            Number of seconds of movement before Low
                            Notification
                        </Text>
                        <Slider
                            min={1}
                            max={notificationDict[user].movNumHigh}
                            name="movNumLow"
                            value={notificationDict[user].movNumLow}
                            step={1}
                            color="blue"
                            radius="md"
                            label={(v) => `${v}s`}
                            marks={[
                                { value: 1, label: "1s" },
                                { value: 10, label: "10s" },
                                { value: 30, label: "30s" },
                            ]}
                            onChangeEnd={(v) =>
                                setNotificationDict({
                                    [user]: {
                                        movThres:
                                            notificationDict[user].movThres,
                                        movNumLow: v,
                                        movNumHigh:
                                            notificationDict[user].movNumHigh,
                                        notificationDelay:
                                            notificationDict[user]
                                                .notificationDelay,
                                        enabled: notificationDict[user].enabled,
                                    },
                                })
                            }
                        />
                    </Stack>
                    <Stack
                        h={300}
                        bg="var(--mantine-color-body)"
                        align="stretch"
                        justify="flex-start"
                        gap="xs"
                    >
                        <Text>
                            Number of seconds of movement before High
                            Notification
                        </Text>
                        <Slider
                            min={notificationDict[user].movNumLow}
                            max={60}
                            name="movNumHigh"
                            value={notificationDict[user].movNumHigh}
                            step={1}
                            color="blue"
                            radius="md"
                            onChangeEnd={(v) =>
                                setNotificationDict({
                                    [user]: {
                                        movThres:
                                            notificationDict[user].movThres,
                                        movNumLow:
                                            notificationDict[user].movNumLow,
                                        movNumHigh: v,
                                        notificationDelay:
                                            notificationDict[user]
                                                .notificationDelay,
                                        enabled: notificationDict[user].enabled,
                                    },
                                })
                            }
                            label={(v) => `${v}s`}
                            marks={[
                                { value: 1, label: "1s" },
                                { value: 30, label: "30s" },
                                { value: 60, label: "60s" },
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
                        <Text>Number of minutes between Low Notifications</Text>
                        <Slider
                            min={60}
                            max={3600}
                            step={60}
                            name="notificationDelay"
                            value={notificationDict[user].notificationDelay}
                            color="blue"
                            radius="md"
                            onChangeEnd={(v) =>
                                setNotificationDict({
                                    [user]: {
                                        movThres:
                                            notificationDict[user].movThres,
                                        movNumLow:
                                            notificationDict[user].movNumLow,
                                        movNumHigh:
                                            notificationDict[user].movNumHigh,
                                        notificationDelay: v,
                                        enabled: notificationDict[user].enabled,
                                    },
                                })
                            }
                            label={(v) => `${v / 60}m`}
                            marks={[
                                { value: 60, label: "1m" },
                                { value: 1800, label: "30m" },
                                { value: 3600, label: "60m" },
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
                            onClick={applyVideo}
                        >
                            Apply
                        </Button>
                        <Button
                            variant="filled"
                            color="green"
                            size="md"
                            radius="lg"
                            onClick={cancelVideo}
                        >
                            Cancel
                        </Button>
                        <Button
                            variant="filled"
                            color="red"
                            size="md"
                            radius="lg"
                            onClick={resetVideo}
                        >
                            Reset
                        </Button>
                    </Flex>
                </Stack>
            </Stack>
        </Box>
    );
}
