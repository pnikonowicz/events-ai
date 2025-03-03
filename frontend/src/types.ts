
export type UniqueEvent = {
  image: string;
  link: string;
  title: string;
  similar_events: {
    image: string;
    link: string;
    title: string;
  }[];
}