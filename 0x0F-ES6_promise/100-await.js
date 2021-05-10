import { createUser, uploadPhoto } from './utils';

export default async function asyncUploadUser() {
  let photo = null;
  let user = null;
  photo = await uploadPhoto();
  user = await createUser();
  return { photo, user };
}
