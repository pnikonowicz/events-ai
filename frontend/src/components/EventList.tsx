import EventItem from "./EventItem"
import { UniqueEvent } from "../types"
import uniqueEventList from '../../../data/unique.json'

function EventList() {
  console.log(uniqueEventList)
  return (
    <ul>
      {uniqueEventList.map((uniqueEvent: UniqueEvent) => (
        <EventItem uniqueEvent={uniqueEvent} key={`${uniqueEvent.title}${uniqueEvent.link}`} />
      ))}
    </ul>
  )
}

export default EventList
