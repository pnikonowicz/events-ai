import { UniqueEvent } from "../types"

function EventItem({ uniqueEvent }: { uniqueEvent: UniqueEvent }) {
  return (
    <li>{uniqueEvent.title}</li>
  )
}

export default EventItem