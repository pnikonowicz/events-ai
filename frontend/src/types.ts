

export type UniqueEvent = {
  image: string | null;
  link: string;
  title: string;
  time: string | null;
  location: string | null;
  similar_events?: UniqueEvent[];
}
