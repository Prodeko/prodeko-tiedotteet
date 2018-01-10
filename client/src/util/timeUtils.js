
/* is the given date lass than three days ago? */
export const isNew = (dateStr) => {
  const today = new Date()
  const date = new Date(dateStr)
  const diff = Math.round((today-date)/(1000*60*60*24))
  return diff < 3
}