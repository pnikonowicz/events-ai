import { Group, Image, List, Stack } from '@mantine/core'
import { UniqueEvent } from "../types"

function EventItem({ uniqueEvent }: { uniqueEvent: UniqueEvent }) {
  return (
    <List.Item styles={{
      item: {
        'display': 'block',
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
          width: '100%',
        }
      }}>
        <Stack style={{
          width: '200px',
        }}>
          <Image src={uniqueEvent.image} />
        </Stack>
        <Stack style={{
          display: 'flex',
          justifyContent: 'flex-start'
        }}>
          {uniqueEvent.title}
        </Stack>
      </Group>
    </List.Item>
  )
}

export default EventItem