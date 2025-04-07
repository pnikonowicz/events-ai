import { Anchor, Group, Image, List, Stack, Text } from '@mantine/core'
import { UniqueEvent } from "../types"

function EventItem({ uniqueEvent }: { uniqueEvent: UniqueEvent }) {
  return (
    <List.Item styles={{
      item: {
        'display': 'flex',
        'width': '100%',
        'padding': '1.5rem',
        'margin': '1rem',
        'borderRadius': '1rem',
        'background': 'var(--mantine-color-blue-8)',
      },
      itemWrapper: {
        width: '100%',
      }
    }}>
      <Group component="div" styles={{
        root: {
          alignItems: 'flex-start',
          width: '100%',
        }
      }}>
        <Stack style={{

          width: '200px',
          height: '100px',
          background: '#000',
          border: '1px solid #000',
          overflow: 'hidden',
        }}>
          <Image src={uniqueEvent.image} />
        </Stack>
        <Stack style={{
          justifyContent: 'flex-start',
          alignSelf: 'flex-start',
          gap: 0,
          textAlign: 'left',
        }}>
          <Group>
            <Text c="#cccccc" size="xs">Location: {uniqueEvent.location || 'N/A'}</Text>
            <Text c="#cccccc" size="xs">Time: {uniqueEvent.time || 'N/A'}</Text>
          </Group>
          <Text component="h3">
            <Anchor href={uniqueEvent.link} c="#fff">
              {uniqueEvent.title}
            </Anchor>
          </Text>
          <Stack>
            <Text c="#cccccc" size="xs">There are {uniqueEvent.similar_events.length || 0} similar events.</Text>
            {uniqueEvent.similar_events.length > 0 && (
              <Stack gap="0">
                <Text size="xs">Show Events</Text>
                <Stack gap="0">
                  {uniqueEvent.similar_events.map((uniqueEvent) => (
                    <Anchor href={uniqueEvent.link} target="_blank" c="#fff" size="xs" fs="italic">{uniqueEvent.title}</Anchor>
                  ))}
                </Stack>
              </Stack>
            )}
          </Stack>
        </Stack>
      </Group>
    </List.Item>
  )
}

export default EventItem