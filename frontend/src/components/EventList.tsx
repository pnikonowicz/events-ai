import { List } from '@mantine/core'
import EventItem from "./EventItem"
import { UniqueEvent } from "../types"
import uniqueEventList from '../../../data/unique.json'

function EventList() {
  console.log(uniqueEventList)
  return (
    <List listStyleType="none">
      {uniqueEventList.map((uniqueEvent: UniqueEvent) => (
        <EventItem uniqueEvent={uniqueEvent} key={`${uniqueEvent.title}${uniqueEvent.link}`} />
      ))}
    </List>
  )
}

export default EventList
