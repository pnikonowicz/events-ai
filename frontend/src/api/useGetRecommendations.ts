
// import axios from 'axios'
// import { useQuery } from '@tanstack/react-query'

// export const useFetchRecommendations = () => {
//   return useQuery({
//     queryKey: ['recommendations'],
//     queryFn: async () => {
//       try {
//         const req = await axios.get('../../../../data/unique.json', {
//           headers: {
//             'Content-Type': 'application/json'
//           }
//         })
//         return req.data
//       } catch (error) {
//         console.log(error)
//       }
//     }
//   })
// }