import { ProgressBar, ProgressIndicator } from "@/components/ui/progress-bar";
import Image from "next/image";
import type { User } from "next-auth";
import React from "react";
import { getParticipantUser } from "../../actions";

export default function RaceTrackerMultiplayer({ position, participantId }: {
  position: number;
  participantId: string
}) {
  const [participantUser, setParticipantUser] = React.useState<
    User | undefined
  >(undefined);

  async function fetchParticipantUser() {
    if (participantId) {
      const user = await getParticipantUser({ participantId });
      if (user) {
        setParticipantUser(user as User);
      }
    }
  }
  React.useEffect(() => void fetchParticipantUser(), [participantId]);

  return (
    <div className="relative flex items-center mb-5">
      <ProgressBar>
        <ProgressIndicator progress={position}>
          <Image
            className="absolute left-0 top-[-50%] border-2 border-monochrome rounded-full transition-all duration-100"
            src={
              participantUser?.image ?? "/placeholder-image.jpg"
            }
            alt={
              `${participantUser?.name} avatar` ?? "user avatar"
            }
            height={30}
            width={30}
            style={{ left: `${position}%` }}
          />
        </ProgressIndicator>
      </ProgressBar>
    </div>
  );
}
